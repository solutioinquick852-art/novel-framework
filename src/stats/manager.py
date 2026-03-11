#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数值系统管理器
管理角色数值、技能、装备等数据
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class StatsManager:
    """数值系统管理器"""
    
    def __init__(self, project_root: str = None):
        """
        初始化数值管理器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root or PROJECT_ROOT)
        self.data_dir = self.project_root / "data"
        self.snapshots_dir = self.data_dir / "stats" / "snapshots"
        self.formulas_path = self.data_dir / "stats" / "formulas.yaml"
        
        self.formulas = self._load_formulas()
        self.snapshots_cache = {}
    
    def _load_formulas(self) -> dict:
        """加载计算公式"""
        if self.formulas_path.exists():
            with open(self.formulas_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _load_snapshot_file(self, file_path: Path) -> dict:
        """
        加载快照文件
        
        Args:
            file_path: 快照文件路径
        
        Returns:
            快照数据
        """
        if str(file_path) in self.snapshots_cache:
            return self.snapshots_cache[str(file_path)]
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
                self.snapshots_cache[str(file_path)] = data
                return data
        
        return {}
    
    def _find_snapshot_file(self, chapter: int) -> Optional[Path]:
        """
        查找包含指定章节的快照文件
        
        Args:
            chapter: 章节号
        
        Returns:
            快照文件路径或None
        """
        for snapshot_file in self.snapshots_dir.glob("ch_*.yaml"):
            # 从文件名提取范围
            match = re.search(r'ch_(\d+)-(\d+)', snapshot_file.stem)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                if start <= chapter <= end:
                    return snapshot_file
        return None
    
    def get_character_snapshot(self, character_id: str, chapter: int) -> dict:
        """
        获取角色在指定章节的数值快照
        
        Args:
            character_id: 角色ID
            chapter: 章节号
        
        Returns:
            角色数值数据
        """
        snapshot_file = self._find_snapshot_file(chapter)
        if not snapshot_file:
            return {}
        
        data = self._load_snapshot_file(snapshot_file)
        characters = data.get("characters", {})
        
        if character_id not in characters:
            return {}
        
        # 找到最接近但不大于目标章节的快照
        char_data = characters[character_id]
        result = {}
        
        for key, value in sorted(char_data.items()):
            if key.startswith("chapter_"):
                chapter_num = int(key.replace("chapter_", ""))
                if chapter_num <= chapter:
                    result = value.copy()
            else:
                result[key] = value
        
        return result
    
    def update_character_snapshot(self, character_id: str, chapter: int, 
                                   stats: dict, reason: str = None) -> bool:
        """
        更新角色数值快照
        
        Args:
            character_id: 角色ID
            chapter: 章节号
            stats: 要更新的数值
            reason: 更新原因
        
        Returns:
            是否成功
        """
        snapshot_file = self._find_snapshot_file(chapter)
        if not snapshot_file:
            # 需要创建新的快照文件
            range_start = ((chapter - 1) // 10) * 10 + 1
            range_end = range_start + 9
            snapshot_file = self.snapshots_dir / f"ch_{range_start:03d}-{range_end:03d}.yaml"
        
        data = self._load_snapshot_file(snapshot_file)
        
        if "range" not in data:
            match = re.search(r'ch_(\d+)-(\d+)', snapshot_file.stem)
            if match:
                data["range"] = {
                    "start": int(match.group(1)),
                    "end": int(match.group(2))
                }
        
        if "characters" not in data:
            data["characters"] = {}
        
        if character_id not in data["characters"]:
            data["characters"][character_id] = {}
        
        chapter_key = f"chapter_{chapter}"
        if chapter_key not in data["characters"][character_id]:
            data["characters"][character_id][chapter_key] = {}
        
        # 更新数值
        data["characters"][character_id][chapter_key].update(stats)
        
        # 添加变更记录
        if reason:
            if "changes" not in data["characters"][character_id][chapter_key]:
                data["characters"][character_id][chapter_key]["changes"] = []
            data["characters"][character_id][chapter_key]["changes"].append({
                "chapter": chapter,
                "type": "update",
                "description": reason,
            })
        
        # 保存文件
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        # 清除缓存
        if str(snapshot_file) in self.snapshots_cache:
            del self.snapshots_cache[str(snapshot_file)]
        
        return True
    
    def calculate_damage(self, attacker_stats: dict, skill_id: str = None) -> int:
        """
        计算技能伤害
        
        Args:
            attacker_stats: 攻击者数值
            skill_id: 技能ID（可选，默认普通攻击）
        
        Returns:
            伤害值
        """
        attack = attacker_stats.get("attributes", {}).get("attack", 10)
        level = attacker_stats.get("level", 1)
        
        if skill_id:
            # 查找技能公式
            skills = self.formulas.get("skills", [])
            for skill in skills:
                if skill.get("id") == skill_id:
                    formula = skill.get("formula", "attack * 1.0")
                    # 简单的公式计算（实际应用中可能需要更复杂的解析）
                    try:
                        damage = eval(formula, {"attack": attack, "level": level})
                        return int(damage)
                    except:
                        return attack
        
        # 默认普通攻击
        return attack
    
    def validate_consistency(self, character_id: str = None) -> List[dict]:
        """
        验证数值一致性
        
        Args:
            character_id: 角色ID（可选，不指定则验证所有角色）
        
        Returns:
            问题列表
        """
        issues = []
        
        for snapshot_file in sorted(self.snapshots_dir.glob("ch_*.yaml")):
            data = self._load_snapshot_file(snapshot_file)
            characters = data.get("characters", {})
            
            for char_id, char_data in characters.items():
                if character_id and char_id != character_id:
                    continue
                
                # 按章节排序检查
                chapters = []
                for key in char_data:
                    if key.startswith("chapter_"):
                        chapter_num = int(key.replace("chapter_", ""))
                        chapters.append((chapter_num, char_data[key]))
                
                chapters.sort(key=lambda x: x[0])
                
                # 检查数值跳跃
                for i in range(1, len(chapters)):
                    prev_chapter, prev_stats = chapters[i-1]
                    curr_chapter, curr_stats = chapters[i]
                    
                    # 检查等级跳跃
                    prev_level = prev_stats.get("level", 0)
                    curr_level = curr_stats.get("level", 0)
                    if curr_level < prev_level:
                        issues.append({
                            "type": "level_decrease",
                            "character": char_id,
                            "from_chapter": prev_chapter,
                            "to_chapter": curr_chapter,
                            "message": f"等级从 {prev_level} 降到 {curr_level}",
                        })
                    
                    # 检查攻击力跳跃（超过50%）
                    prev_attack = prev_stats.get("attributes", {}).get("attack", 0)
                    curr_attack = curr_stats.get("attributes", {}).get("attack", 0)
                    if prev_attack > 0 and curr_attack > prev_attack * 1.5:
                        # 检查是否有变更说明
                        changes = curr_stats.get("changes", [])
                        has_explanation = any(
                            c.get("type") in ["突破", "装备", "upgrade"]
                            for c in changes
                        )
                        if not has_explanation:
                            issues.append({
                                "type": "attack_jump",
                                "character": char_id,
                                "from_chapter": prev_chapter,
                                "to_chapter": curr_chapter,
                                "message": f"攻击力从 {prev_attack} 跳到 {curr_attack}，缺少说明",
                            })
        
        return issues
    
    def get_all_characters(self) -> List[str]:
        """
        获取所有有数值记录的角色ID
        
        Returns:
            角色ID列表
        """
        characters = set()
        
        for snapshot_file in self.snapshots_dir.glob("ch_*.yaml"):
            data = self._load_snapshot_file(snapshot_file)
            characters.update(data.get("characters", {}).keys())
        
        return sorted(characters)


def main():
    """测试入口"""
    manager = StatsManager()
    
    # 测试获取数值
    stats = manager.get_character_snapshot("ye_fan", 1)
    print("叶凡第1章数值：")
    print(yaml.dump(stats, allow_unicode=True, default_flow_style=False))
    
    # 测试一致性验证
    issues = manager.validate_consistency()
    if issues:
        print("\n一致性问题：")
        for issue in issues:
            print(f"  - {issue['message']}")
    else:
        print("\n✓ 数值一致性检查通过")


if __name__ == "__main__":
    main()
