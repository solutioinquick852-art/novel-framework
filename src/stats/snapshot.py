#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快照管理器
管理数值快照的创建和查询
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class SnapshotManager:
    """快照管理器"""
    
    def __init__(self, project_root: str = None):
        """
        初始化快照管理器
        
        Args:
            project_root: 项目根目录
        """
        from pathlib import Path
        self.project_root = Path(project_root or Path.cwd())
        self.snapshots_dir = self.project_root / "data" / "stats" / "snapshots"
    
    def create_snapshot(self, chapter: int, character_id: str, 
                        stats: dict, changes: List[dict] = None) -> bool:
        """
        创建数值快照
        
        Args:
            chapter: 章节号
            character_id: 角色ID
            stats: 角色数值
            changes: 变更列表
        
        Returns:
            是否成功
        """
        # 确定快照文件
        range_start = ((chapter - 1) // 10) * 10 + 1
        range_end = range_start + 9
        snapshot_file = self.snapshots_dir / f"ch_{range_start:03d}-{range_end:03d}.yaml"
        
        # 加载或创建数据
        if snapshot_file.exists():
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {
                "range": {"start": range_start, "end": range_end},
                "characters": {}
            }
        
        # 更新数据
        if "characters" not in data:
            data["characters"] = {}
        
        if character_id not in data["characters"]:
            data["characters"][character_id] = {}
        
        chapter_key = f"chapter_{chapter}"
        snapshot_data = stats.copy()
        
        if changes:
            snapshot_data["changes"] = changes
        
        snapshot_data["snapshot_time"] = datetime.now().isoformat()
        
        data["characters"][character_id][chapter_key] = snapshot_data
        
        # 保存
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        return True
    
    def get_snapshot(self, character_id: str, chapter: int) -> Optional[dict]:
        """
        获取快照
        
        Args:
            character_id: 角色ID
            chapter: 章节号
        
        Returns:
            快照数据或None
        """
        # 查找对应的快照文件
        for snapshot_file in self.snapshots_dir.glob("ch_*.yaml"):
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            range_info = data.get("range", {})
            if range_info.get("start", 0) <= chapter <= range_info.get("end", float('inf')):
                char_data = data.get("characters", {}).get(character_id, {})
                chapter_key = f"chapter_{chapter}"
                return char_data.get(chapter_key)
        
        return None
    
    def list_snapshots(self, character_id: str = None) -> List[dict]:
        """
        列出所有快照
        
        Args:
            character_id: 角色ID（可选）
        
        Returns:
            快照列表
        """
        snapshots = []
        
        for snapshot_file in sorted(self.snapshots_dir.glob("ch_*.yaml")):
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            range_info = data.get("range", {})
            characters = data.get("characters", {})
            
            for char_id, char_data in characters.items():
                if character_id and char_id != character_id:
                    continue
                
                for key, value in char_data.items():
                    if key.startswith("chapter_"):
                        chapter = int(key.replace("chapter_", ""))
                        snapshots.append({
                            "file": str(snapshot_file),
                            "range": range_info,
                            "character": char_id,
                            "chapter": chapter,
                            "data": value,
                        })
        
        return sorted(snapshots, key=lambda x: (x["character"], x["chapter"]))
