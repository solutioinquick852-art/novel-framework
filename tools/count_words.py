#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字数统计工具
用于统计小说的字数、章节数等信息
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class WordCounter:
    """字数统计器"""
    
    def __init__(self, project_root: str = None):
        """
        初始化字数统计器
        
        Args:
            project_root: 项目根目录，默认为当前目录
        """
        self.project_root = Path(project_root or PROJECT_ROOT)
        self.content_dir = self.project_root / "content" / "volumes"
        self.reports_dir = self.project_root / "reports" / "stats"
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = self.project_root / ".novel" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def count_chinese_chars(self, text: str) -> int:
        """
        统计中文字符数
        
        Args:
            text: 要统计的文本
        
        Returns:
            中文字符数
        """
        # 匹配中文字符（包括标点）
        chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        return len(chinese_pattern.findall(text))
    
    def extract_chapter_content(self, file_path: Path) -> tuple:
        """
        提取章节内容，移除YAML front matter和注释
        
        Args:
            file_path: 章节文件路径
        
        Returns:
            (元数据, 内容) 元组
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML front matter
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1]) or {}
                except:
                    pass
                content = parts[2]
        
        # 移除HTML注释
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # 移除Markdown标题标记（但保留内容）
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        
        # 移除多余空白
        content = content.strip()
        
        return metadata, content
    
    def count_chapter(self, chapter_path: Path) -> dict:
        """
        统计单个章节
        
        Args:
            chapter_path: 章节路径
        
        Returns:
            统计结果
        """
        metadata, content = self.extract_chapter_content(chapter_path)
        
        word_count = self.count_chinese_chars(content)
        
        return {
            "file": str(chapter_path.relative_to(self.project_root)),
            "chapter": metadata.get("chapter", 0),
            "title": metadata.get("title", chapter_path.stem),
            "word_count": word_count,
            "status": metadata.get("status", "unknown"),
        }
    
    def count_volume(self, volume_path: Path) -> dict:
        """
        统计整卷
        
        Args:
            volume_path: 卷目录路径
        
        Returns:
            统计结果
        """
        chapters = []
        total_words = 0
        
        # 查找所有章节文件
        chapter_files = sorted(volume_path.glob("ch_*.md"))
        
        for chapter_file in chapter_files:
            result = self.count_chapter(chapter_file)
            chapters.append(result)
            total_words += result["word_count"]
        
        return {
            "volume": volume_path.name,
            "chapters": chapters,
            "total_words": total_words,
            "chapter_count": len(chapters),
            "average_words": total_words // len(chapters) if chapters else 0,
        }
    
    def count_all(self) -> dict:
        """
        统计所有卷
        
        Returns:
            完整统计结果
        """
        volumes = []
        total_words = 0
        total_chapters = 0
        
        # 统计各卷
        for volume_dir in sorted(self.content_dir.iterdir()):
            if volume_dir.is_dir():
                result = self.count_volume(volume_dir)
                volumes.append(result)
                total_words += result["total_words"]
                total_chapters += result["chapter_count"]
        
        # 获取目标字数
        target_words = self.config.get("novel", {}).get("target_words", 3000000)
        
        return {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_words": total_words,
                "total_chapters": total_chapters,
                "target_words": target_words,
                "progress_percent": round(total_words / target_words * 100, 2) if target_words > 0 else 0,
                "average_per_chapter": total_words // total_chapters if total_chapters > 0 else 0,
            },
            "volumes": volumes,
        }
    
    def generate_report(self, output_format: str = "text") -> str:
        """
        生成统计报告
        
        Args:
            output_format: 输出格式 (text/json/yaml)
        
        Returns:
            报告内容
        """
        stats = self.count_all()
        
        if output_format == "json":
            return json.dumps(stats, ensure_ascii=False, indent=2)
        
        if output_format == "yaml":
            return yaml.dump(stats, allow_unicode=True, default_flow_style=False)
        
        # 文本格式
        lines = []
        lines.append("=" * 50)
        lines.append("字数统计")
        lines.append("=" * 50)
        lines.append("")
        
        summary = stats["summary"]
        lines.append(f"总计：{summary['total_words']:,} 字 ({summary['total_chapters']} 章)")
        lines.append(f"目标：{summary['target_words']:,} 字")
        lines.append(f"进度：{summary['progress_percent']}%")
        lines.append(f"平均：{summary['average_per_chapter']} 字/章")
        lines.append("")
        
        lines.append("分卷统计：")
        for vol in stats["volumes"]:
            lines.append(f"  {vol['volume']}: {vol['total_words']:,} 字 ({vol['chapter_count']} 章)")
        
        lines.append("")
        lines.append(f"统计时间：{stats['generated_at']}")
        
        return "\n".join(lines)
    
    def save_report(self, output_path: Path = None):
        """
        保存报告到文件
        
        Args:
            output_path: 输出路径，默认为 reports/stats/word_count.md
        """
        if output_path is None:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.reports_dir / "word_count.md"
        
        report = self.generate_report("text")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 同时保存JSON格式
        json_path = output_path.with_suffix('.json')
        json_report = self.generate_report("json")
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_report)
        
        return output_path


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='字数统计工具')
    parser.add_argument('--project', '-p', help='项目路径')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'yaml'], 
                        default='text', help='输出格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--save', '-s', action='store_true', help='保存报告')
    parser.add_argument('--quick', '-q', action='store_true', help='快速模式（只输出总字数）')
    
    args = parser.parse_args()
    
    counter = WordCounter(args.project)
    
    if args.quick:
        stats = counter.count_all()
        print(stats["summary"]["total_words"])
    elif args.save:
        output_path = counter.save_report(Path(args.output) if args.output else None)
        print(f"✓ 报告已保存：{output_path}")
    else:
        report = counter.generate_report(args.format)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ 已保存到：{args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
