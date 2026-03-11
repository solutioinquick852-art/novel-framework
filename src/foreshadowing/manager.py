#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伏笔管理器
管理伏笔的完整生命周期：埋设、强化、揭示、放弃
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class ForeshadowingManager:
    """伏笔管理器"""
    
    # 状态定义
    STATUS_PLANTED = "planted"      # 已埋下
    STATUS_HINTED = "hinted"        # 已强化
    STATUS_READY = "ready"          # 准备揭示
    STATUS_REVEALED = "revealed"    # 已揭示
    STATUS_ABANDONED = "abandoned"  # 已放弃
    
    # 重要性级别
    IMPORTANCE_CRITICAL = "critical"
    IMPORTANCE_MAJOR = "major"
    IMPORTANCE_MINOR = "minor"
    
    # 类型定义
    TYPES = ["道具", "角色", "事件", "设定"]
    
    def __init__(self, project_root: str = None):
        """
        初始化伏笔管理器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root or PROJECT_ROOT)
        self.data_dir = self.project_root / "data" / "foreshadowing"
        self.active_file = self.data_dir / "active.yaml"
        self.completed_file = self.data_dir / "completed.yaml"
        self.config = self._load_config()
        
        # 确保数据目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> dict:
        """加载配置"""
        config_path = self.project_root / ".novel" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _load_active(self) -> dict:
        """加载活跃伏笔"""
        if self.active_file.exists():
            with open(self.active_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {"foreshadowing": []}
        return {"foreshadowing": []}
    
    def _save_active(self, data: dict):
        """保存活跃伏笔"""
        with open(self.active_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    def _load_completed(self) -> dict:
        """加载已完成伏笔"""
        if self.completed_file.exists():
            with open(self.completed_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {"foreshadowing": []}
        return {"foreshadowing": []}
    
    def _save_completed(self, data: dict):
        """保存已完成伏笔"""
        with open(self.completed_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    def _generate_id(self) -> str:
        """生成伏笔ID"""
        import re
        # 找到当前最大的ID号
        data = self._load_active()
        max_num = 0
        
        for fs in data.get("foreshadowing", []):
            fs_id = fs.get("id", "")
            match = re.search(r'fs_(\d+)', fs_id)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
        
        return f"fs_{max_num + 1:03d}"
    
    def _calculate_urgency(self, fs: dict, current_chapter: int = None) -> str:
        """
        计算伏笔紧急度
        
        Args:
            fs: 伏笔数据
            current_chapter: 当前章节
        
        Returns:
            紧急度 (low/medium/high/critical)
        """
        if current_chapter is None:
            current_chapter = self._get_latest_chapter()
        
        planted_chapter = fs.get("planted", {}).get("chapter", 0)
        chapters_since = current_chapter - planted_chapter
        
        target_range = fs.get("reveal", {}).get("target_range", [0, 999999])
        importance = fs.get("importance", "minor")
        
        # 根据重要性和时间计算紧急度
        importance_thresholds = self.config.get("foreshadowing", {}).get(
            "importance_levels", {"critical": 30, "major": 60, "minor": 100}
        )
        
        threshold = importance_thresholds.get(importance, 100)
        
        if chapters_since >= threshold:
            return "critical"
        elif chapters_since >= threshold * 0.8:
            return "high"
        elif chapters_since >= threshold * 0.5:
            return "medium"
        else:
            return "low"
    
    def _get_latest_chapter(self) -> int:
        """获取最新章节号"""
        content_dir = self.project_root / "content" / "volumes"
        if not content_dir.exists():
            return 0
        
        import re
        max_chapter = 0
        for chapter_file in content_dir.glob("**/ch_*.md"):
            match = re.search(r'ch_(\d+)', chapter_file.stem)
            if match:
                chapter_num = int(match.group(1))
                if chapter_num > max_chapter:
                    max_chapter = chapter_num
        
        return max_chapter
    
    def plant(self, fs_type: str, title: str, chapter: int, 
              description: str, importance: str = "minor",
              target_range: List[int] = None, **kwargs) -> str:
        """
        埋下新伏笔
        
        Args:
            fs_type: 伏笔类型 (道具/角色/事件/设定)
            title: 伏笔标题
            chapter: 埋设章节
            description: 埋设描述
            importance: 重要性 (critical/major/minor)
            target_range: 计划揭示章节范围 [start, end]
            **kwargs: 其他参数
        
        Returns:
            伏笔ID
        """
        if fs_type not in self.TYPES:
            raise ValueError(f"无效的伏笔类型: {fs_type}")
        
        if importance not in [self.IMPORTANCE_CRITICAL, self.IMPORTANCE_MAJOR, self.IMPORTANCE_MINOR]:
            raise ValueError(f"无效的重要性级别: {importance}")
        
        fs_id = self._generate_id()
        
        fs_data = {
            "id": fs_id,
            "type": fs_type,
            "title": title,
            "importance": importance,
            "planted": {
                "chapter": chapter,
                "description": description,
            },
            "hints": [],
            "reveal": {
                "target_range": target_range or [0, 999999],
                "planned_chapter": None,
                "reveal_type": kwargs.get("reveal_type", "gradual"),
                "description": kwargs.get("reveal_description", ""),
            },
            "status": self.STATUS_PLANTED,
            "last_hint_chapter": None,
            "chapters_since_planted": 0,
            "urgency": "low",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "notes": kwargs.get("notes", ""),
        }
        
        # 添加额外字段
        if "context" in kwargs:
            fs_data["planted"]["context"] = kwargs["context"]
        
        # 加载并保存
        data = self._load_active()
        data["foreshadowing"].append(fs_data)
        self._save_active(data)
        
        return fs_id
    
    def add_hint(self, fs_id: str, chapter: int, content: str,
                 subtlety: str = "moderate") -> bool:
        """
        添加伏笔强化
        
        Args:
            fs_id: 伏笔ID
            chapter: 强化章节
            content: 强化内容
            subtlety: 强度 (subtle/moderate/obvious)
        
        Returns:
            是否成功
        """
        data = self._load_active()
        
        for fs in data.get("foreshadowing", []):
            if fs.get("id") == fs_id:
                hint = {
                    "chapter": chapter,
                    "content": content,
                    "subtlety": subtlety,
                }
                fs["hints"].append(hint)
                fs["last_hint_chapter"] = chapter
                fs["status"] = self.STATUS_HINTED
                fs["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                
                self._save_active(data)
                return True
        
        return False
    
    def reveal(self, fs_id: str, chapter: int, description: str = None) -> bool:
        """
        揭示伏笔
        
        Args:
            fs_id: 伏笔ID
            chapter: 揭示章节
            description: 揭示描述
        
        Returns:
            是否成功
        """
        data = self._load_active()
        completed_data = self._load_completed()
        
        for i, fs in enumerate(data.get("foreshadowing", [])):
            if fs.get("id") == fs_id:
                # 更新状态
                fs["status"] = self.STATUS_REVEALED
                fs["reveal"]["planned_chapter"] = chapter
                fs["reveal"]["actual_chapter"] = chapter
                if description:
                    fs["reveal"]["description"] = description
                fs["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                fs["completed_date"] = datetime.now().strftime("%Y-%m-%d")
                
                # 移动到已完成列表
                completed_data["foreshadowing"].append(fs)
                data["foreshadowing"].pop(i)
                
                self._save_active(data)
                self._save_completed(completed_data)
                return True
        
        return False
    
    def abandon(self, fs_id: str, reason: str = None) -> bool:
        """
        放弃伏笔
        
        Args:
            fs_id: 伏笔ID
            reason: 放弃原因
        
        Returns:
            是否成功
        """
        data = self._load_active()
        
        for fs in data.get("foreshadowing", []):
            if fs.get("id") == fs_id:
                fs["status"] = self.STATUS_ABANDONED
                fs["abandon_reason"] = reason
                fs["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                
                self._save_active(data)
                return True
        
        return False
    
    def get_reminders(self, current_chapter: int = None) -> List[dict]:
        """
        获取当前应提醒的伏笔
        
        Args:
            current_chapter: 当前章节
        
        Returns:
            提醒列表
        """
        if current_chapter is None:
            current_chapter = self._get_latest_chapter()
        
        data = self._load_active()
        reminders = []
        
        reminder_threshold = self.config.get("foreshadowing", {}).get(
            "reminder_threshold", 20
        )
        
        for fs in data.get("foreshadowing", []):
            # 计算紧急度
            urgency = self._calculate_urgency(fs, current_chapter)
            
            # 检查是否需要提醒
            needs_attention = False
            reminder_type = None
            
            # 超过阈值未揭示
            planted_chapter = fs.get("planted", {}).get("chapter", 0)
            chapters_since = current_chapter - planted_chapter
            
            if chapters_since >= reminder_threshold:
                needs_attention = True
                reminder_type = "long_time"
            
            # 超过强化时间
            last_hint = fs.get("last_hint_chapter")
            if last_hint and (current_chapter - last_hint) >= reminder_threshold:
                needs_attention = True
                reminder_type = "need_hint"
            
            # 即将到期
            target_range = fs.get("reveal", {}).get("target_range", [0, 999999])
            if target_range[0] > 0 and current_chapter >= target_range[0] - 10:
                needs_attention = True
                reminder_type = "approaching_deadline"
            
            if needs_attention or urgency in ["high", "critical"]:
                reminders.append({
                    "fs_id": fs.get("id"),
                    "title": fs.get("title"),
                    "type": fs.get("type"),
                    "importance": fs.get("importance"),
                    "urgency": urgency,
                    "chapters_since_planted": chapters_since,
                    "last_hint_chapter": last_hint,
                    "target_range": target_range,
                    "reminder_type": reminder_type,
                })
        
        # 按紧急度和重要性排序
        urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        importance_order = {"critical": 0, "major": 1, "minor": 2}
        
        reminders.sort(key=lambda x: (
            urgency_order.get(x["urgency"], 3),
            importance_order.get(x["importance"], 2)
        ))
        
        return reminders
    
    def get_status_report(self) -> dict:
        """
        获取伏笔状态报告
        
        Returns:
            状态报告
        """
        active_data = self._load_active()
        completed_data = self._load_completed()
        
        active_fs = active_data.get("foreshadowing", [])
        completed_fs = completed_data.get("foreshadowing", [])
        
        # 统计
        status_count = {}
        for fs in active_fs:
            status = fs.get("status", "unknown")
            status_count[status] = status_count.get(status, 0) + 1
        
        type_count = {}
        for fs in active_fs:
            fs_type = fs.get("type", "unknown")
            type_count[fs_type] = type_count.get(fs_type, 0) + 1
        
        importance_count = {}
        for fs in active_fs:
            importance = fs.get("importance", "unknown")
            importance_count[importance] = importance_count.get(importance, 0) + 1
        
        return {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_active": len(active_fs),
                "total_completed": len(completed_fs),
                "by_status": status_count,
                "by_type": type_count,
                "by_importance": importance_count,
            },
            "active_foreshadowing": active_fs,
            "completed_foreshadowing": completed_fs,
        }
    
    def list_all(self, status: str = None, fs_type: str = None,
                 importance: str = None) -> List[dict]:
        """
        列出伏笔
        
        Args:
            status: 筛选状态
            fs_type: 筛选类型
            importance: 筛选重要性
        
        Returns:
            伏笔列表
        """
        data = self._load_active()
        result = []
        
        for fs in data.get("foreshadowing", []):
            if status and fs.get("status") != status:
                continue
            if fs_type and fs.get("type") != fs_type:
                continue
            if importance and fs.get("importance") != importance:
                continue
            
            result.append(fs)
        
        return result


def main():
    """测试入口"""
    manager = ForeshadowingManager()
    
    # 测试埋下伏笔
    print("测试埋下伏笔...")
    fs_id = manager.plant(
        fs_type="道具",
        title="测试伏笔",
        chapter=1,
        description="这是一个测试伏笔",
        importance="major",
        target_range=[50, 100]
    )
    print(f"✓ 埋下伏笔：{fs_id}")
    
    # 测试列出伏笔
    print("\n活跃伏笔：")
    for fs in manager.list_all():
        print(f"  - {fs['id']}: {fs['title']}")
    
    # 测试获取提醒
    print("\n伏笔提醒：")
    reminders = manager.get_reminders(1)
    for r in reminders:
        print(f"  - {r['fs_id']}: {r['title']} (紧急度: {r['urgency']})")


if __name__ == "__main__":
    main()
