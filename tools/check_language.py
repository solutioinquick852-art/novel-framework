#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言检查工具
检查章节中不应出现的英文单词
"""

import os
import sys
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class LanguageLinter:
    """语言检查器"""
    
    def __init__(self, project_root: str = None):
        """
        初始化语言检查器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root or PROJECT_ROOT)
        self.content_dir = self.project_root / "content" / "volumes"
        self.reports_dir = self.project_root / "reports" / "quality"
        self.config = self._load_config()
        self.whitelist = self._load_whitelist()
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = self.project_root / ".novel" / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _load_whitelist(self) -> Set[str]:
        """加载英文白名单"""
        whitelist_path = self.project_root / ".novel" / "whitelist.txt"
        whitelist = set()
        
        if whitelist_path.exists():
            with open(whitelist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if line and not line.startswith('#'):
                        whitelist.add(line.upper())  # 统一转大写
        
        return whitelist
    
    def extract_checkable_content(self, file_path: Path) -> Tuple[dict, str]:
        """
        提取可检查的内容（移除YAML front matter和代码块）
        
        Args:
            file_path: 文件路径
        
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
        
        # 移除代码块
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`[^`]+`', '', content)
        
        # 移除HTML注释
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        return metadata, content
    
    def check_file(self, file_path: Path) -> dict:
        """
        检查单个文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            检查结果
        """
        metadata, content = self.extract_checkable_content(file_path)
        
        # 查找所有英文单词
        english_words = re.findall(r'\b[a-zA-Z]+\b', content)
        
        violations = []
        for word in english_words:
            word_upper = word.upper()
            if word_upper not in self.whitelist:
                # 查找行号
                lines = content.split('\n')
                line_num = 0
                for i, line in enumerate(lines, 1):
                    if word in line:
                        line_num = i
                        break
                
                violations.append({
                    "word": word,
                    "line": line_num,
                    "suggestion": self._get_suggestion(word),
                })
        
        return {
            "file": str(file_path.relative_to(self.project_root)),
            "chapter": metadata.get("chapter", 0),
            "title": metadata.get("title", file_path.stem),
            "violations": violations,
            "violation_count": len(violations),
            "passed": len(violations) == 0,
        }
    
    def _get_suggestion(self, word: str) -> str:
        """
        获取建议的中文替换
        
        Args:
            word: 英文单词
        
        Returns:
            建议的中文
        """
        # 从配置中获取替换映射
        replace_map = self.config.get("language", {}).get("auto_fix", {}).get("replace_map", {})
        return replace_map.get(word.upper(), "")
    
    def check_all(self, chapter_range: Tuple[int, int] = None) -> dict:
        """
        检查所有章节
        
        Args:
            chapter_range: 章节范围 (start, end)
        
        Returns:
            检查结果
        """
        results = []
        passed_count = 0
        failed_count = 0
        total_violations = 0
        
        # 查找所有章节文件
        for volume_dir in sorted(self.content_dir.iterdir()):
            if volume_dir.is_dir():
                for chapter_file in sorted(volume_dir.glob("ch_*.md")):
                    # 提取章节号
                    match = re.search(r'ch_(\d+)', chapter_file.stem)
                    if match:
                        chapter_num = int(match.group(1))
                        
                        # 检查章节范围
                        if chapter_range:
                            if chapter_num < chapter_range[0] or chapter_num > chapter_range[1]:
                                continue
                        
                        result = self.check_file(chapter_file)
                        results.append(result)
                        
                        if result["passed"]:
                            passed_count += 1
                        else:
                            failed_count += 1
                            total_violations += result["violation_count"]
        
        return {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_chapters": len(results),
                "passed": passed_count,
                "failed": failed_count,
                "pass_rate": round(passed_count / len(results) * 100, 2) if results else 100,
                "total_violations": total_violations,
            },
            "results": results,
        }
    
    def generate_report(self, check_result: dict = None, output_format: str = "text") -> str:
        """
        生成检查报告
        
        Args:
            check_result: 检查结果
            output_format: 输出格式
        
        Returns:
            报告内容
        """
        if check_result is None:
            check_result = self.check_all()
        
        if output_format == "yaml":
            return yaml.dump(check_result, allow_unicode=True, default_flow_style=False)
        
        # 文本格式
        lines = []
        lines.append("# 语言检查报告")
        lines.append("")
        lines.append(f"**检查时间：** {check_result['generated_at']}")
        lines.append("")
        
        summary = check_result["summary"]
        lines.append("## 总体情况")
        lines.append("")
        lines.append(f"- **检查章节数：** {summary['total_chapters']}")
        lines.append(f"- **通过章节数：** {summary['passed']}")
        lines.append(f"- **问题章节数：** {summary['failed']}")
        lines.append(f"- **通过率：** {summary['pass_rate']}%")
        lines.append(f"- **总问题数：** {summary['total_violations']}")
        lines.append("")
        
        # 只显示有问题的章节
        failed_results = [r for r in check_result["results"] if not r["passed"]]
        
        if failed_results:
            lines.append("## 问题详情")
            lines.append("")
            
            for result in failed_results:
                lines.append(f"### {result['file']}")
                lines.append("")
                lines.append(f"**问题数：** {result['violation_count']}")
                lines.append("")
                lines.append("| 行号 | 内容 | 类型 | 建议 |")
                lines.append("|------|------|------|------|")
                
                for v in result["violations"]:
                    suggestion = v.get("suggestion", "")
                    lines.append(f"| {v['line']} | `{v['word']}` | 非白名单英文 | {suggestion} |")
                
                lines.append("")
        
        # 白名单状态
        lines.append("## 白名单状态")
        lines.append("")
        lines.append(f"当前白名单包含 {len(self.whitelist)} 个术语")
        
        return "\n".join(lines)
    
    def save_report(self, output_path: Path = None):
        """
        保存报告到文件
        
        Args:
            output_path: 输出路径
        """
        if output_path is None:
            self.reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.reports_dir / "language_check.md"
        
        check_result = self.check_all()
        report = self.generate_report(check_result, "text")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='语言检查工具')
    parser.add_argument('--project', '-p', help='项目路径')
    parser.add_argument('--chapters', '-c', help='章节范围（如：40-50）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--save', '-s', action='store_true', help='保存报告')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    linter = LanguageLinter(args.project)
    
    # 解析章节范围
    chapter_range = None
    if args.chapters:
        parts = args.chapters.split('-')
        if len(parts) == 2:
            chapter_range = (int(parts[0]), int(parts[1]))
    
    check_result = linter.check_all(chapter_range)
    
    if args.save:
        output_path = linter.save_report(Path(args.output) if args.output else None)
        print(f"✓ 报告已保存：{output_path}")
    elif args.quiet:
        # 只输出是否通过
        if check_result["summary"]["failed"] == 0:
            print("✓ 通过")
            sys.exit(0)
        else:
            print(f"✗ 发现 {check_result['summary']['total_violations']} 个问题")
            sys.exit(1)
    else:
        report = linter.generate_report(check_result, "text")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ 已保存到：{args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()
