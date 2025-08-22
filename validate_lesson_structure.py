#!/usr/bin/env python3
"""
Lesson Structure Validation and Migration Tool
==============================================

This script validates lesson JSON files against the standardized structure
and provides migration capabilities for updating existing lessons.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add the app directory to Python path
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

class LessonValidator:
    """Validates lesson JSON structure against standards"""
    
    def __init__(self):
        self.required_fields = {
            'id': str,
            'title': str,
            'description': str,
            'tag': str,
            'xp_reward': int,
            'difficulty': str,
            'intro': dict,
            'sections': dict
        }
        
        self.valid_difficulties = ['beginner', 'intermediate', 'advanced', 'expert']
        self.xp_range = (50, 150)
        
        self.required_intro_fields = {
            'main': str
        }
        
        self.required_sections = {
            'learning': dict
        }
        
        self.optional_sections = {
            'opening_quiz': dict,
            'reflection': dict,
            'application': dict,
            'closing_quiz': dict,
            'summary': dict
        }
        
    def validate_lesson(self, lesson_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Validate a lesson against the standard structure
        
        Returns:
            Dictionary with 'errors', 'warnings', and 'suggestions' lists
        """
        result = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Check required top-level fields
        for field, expected_type in self.required_fields.items():
            if field not in lesson_data:
                result['errors'].append(f"Missing required field: {field}")
            elif not isinstance(lesson_data[field], expected_type):
                result['errors'].append(f"Field '{field}' should be {expected_type.__name__}, got {type(lesson_data[field]).__name__}")
        
        # Validate specific fields
        if 'difficulty' in lesson_data:
            if lesson_data['difficulty'] not in self.valid_difficulties:
                result['warnings'].append(f"Difficulty '{lesson_data['difficulty']}' not in standard list: {self.valid_difficulties}")
        
        if 'xp_reward' in lesson_data:
            xp = lesson_data['xp_reward']
            if not (self.xp_range[0] <= xp <= self.xp_range[1]):
                result['warnings'].append(f"XP reward {xp} outside recommended range {self.xp_range}")
        
        # Validate intro section
        if 'intro' in lesson_data:
            intro = lesson_data['intro']
            for field, expected_type in self.required_intro_fields.items():
                if field not in intro:
                    result['errors'].append(f"Missing required intro field: {field}")
                elif not isinstance(intro[field], expected_type):
                    result['errors'].append(f"Intro field '{field}' should be {expected_type.__name__}")
        
        # Validate sections
        if 'sections' in lesson_data:
            sections = lesson_data['sections']
            
            # Check required sections
            for section, expected_type in self.required_sections.items():
                if section not in sections:
                    result['errors'].append(f"Missing required section: {section}")
                elif not isinstance(sections[section], expected_type):
                    result['errors'].append(f"Section '{section}' should be {expected_type.__name__}")
            
            # Check learning section structure
            if 'learning' in sections and isinstance(sections['learning'], dict):
                if 'sections' not in sections['learning']:
                    result['errors'].append("Learning section missing 'sections' array")
                elif not isinstance(sections['learning']['sections'], list):
                    result['errors'].append("Learning 'sections' should be an array")
                else:
                    for i, learning_section in enumerate(sections['learning']['sections']):
                        if not isinstance(learning_section, dict):
                            result['errors'].append(f"Learning section {i} should be an object")
                        else:
                            if 'title' not in learning_section:
                                result['errors'].append(f"Learning section {i} missing 'title'")
                            if 'content' not in learning_section:
                                result['errors'].append(f"Learning section {i} missing 'content'")
            
            # Check quiz sections structure
            for quiz_section in ['opening_quiz', 'closing_quiz']:
                if quiz_section in sections:
                    self._validate_quiz_section(sections[quiz_section], quiz_section, result)
        
        # Suggestions for missing optional sections
        if 'sections' in lesson_data:
            sections = lesson_data['sections']
            if 'opening_quiz' not in sections:
                result['suggestions'].append("Consider adding an opening quiz for pre-assessment")
            if 'reflection' not in sections:
                result['suggestions'].append("Consider adding reflection exercises")
            if 'application' not in sections:
                result['suggestions'].append("Consider adding practical application exercises")
            if 'closing_quiz' not in sections:
                result['suggestions'].append("Consider adding a closing quiz for assessment")
        
        return result
    
    def _validate_quiz_section(self, quiz_data: Dict, section_name: str, result: Dict[str, List[str]]):
        """Validate quiz section structure"""
        required_quiz_fields = ['title', 'description', 'questions']
        
        for field in required_quiz_fields:
            if field not in quiz_data:
                result['errors'].append(f"{section_name} missing required field: {field}")
        
        if 'questions' in quiz_data and isinstance(quiz_data['questions'], list):
            for i, question in enumerate(quiz_data['questions']):
                if not isinstance(question, dict):
                    result['errors'].append(f"{section_name} question {i} should be an object")
                    continue
                
                required_question_fields = ['question', 'options', 'explanation']
                for field in required_question_fields:
                    if field not in question:
                        result['errors'].append(f"{section_name} question {i} missing field: {field}")
                
                if 'options' in question and not isinstance(question['options'], list):
                    result['errors'].append(f"{section_name} question {i} 'options' should be an array")

class LessonMigrator:
    """Migrates lessons to new standard structure"""
    
    def migrate_lesson(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migrate a lesson to the standard structure
        
        Returns:
            Migrated lesson data
        """
        migrated = lesson_data.copy()
        
        # Standardize difficulty
        if 'difficulty' in migrated:
            difficulty = migrated['difficulty'].lower()
            if difficulty == 'basic' or difficulty == 'beginner':
                migrated['difficulty'] = 'beginner'
            elif difficulty == 'medium' or difficulty == 'intermediate':
                migrated['difficulty'] = 'intermediate'
            elif difficulty == 'hard' or difficulty == 'advanced':
                migrated['difficulty'] = 'advanced'
            elif difficulty == 'expert' or difficulty == 'master':
                migrated['difficulty'] = 'expert'
        
        # Ensure XP reward is within reasonable range
        if 'xp_reward' in migrated:
            xp = migrated['xp_reward']
            if xp < 50:
                migrated['xp_reward'] = 50
            elif xp > 150:
                migrated['xp_reward'] = 150
        
        # Add missing optional fields with defaults
        if 'estimated_time' not in migrated:
            migrated['estimated_time'] = "20-25 minutes"
        
        # Ensure intro has required structure
        if 'intro' in migrated and isinstance(migrated['intro'], dict):
            if 'main' not in migrated['intro'] and 'content' in migrated['intro']:
                migrated['intro']['main'] = migrated['intro'].pop('content')
        
        return migrated

def validate_lesson_file(file_path: str) -> Dict[str, Any]:
    """
    Validate a single lesson file
    
    Returns:
        Validation results with file info
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lesson_data = json.load(f)
        
        validator = LessonValidator()
        validation_result = validator.validate_lesson(lesson_data)
        
        return {
            'file': file_path,
            'valid': len(validation_result['errors']) == 0,
            'lesson_id': lesson_data.get('id', 'Unknown'),
            'title': lesson_data.get('title', 'Unknown'),
            'errors': validation_result['errors'],
            'warnings': validation_result['warnings'],
            'suggestions': validation_result['suggestions']
        }
        
    except json.JSONDecodeError as e:
        return {
            'file': file_path,
            'valid': False,
            'lesson_id': 'Unknown',
            'title': 'Unknown',
            'errors': [f"JSON decode error: {str(e)}"],
            'warnings': [],
            'suggestions': []
        }
    except Exception as e:
        return {
            'file': file_path,
            'valid': False,
            'lesson_id': 'Unknown',
            'title': 'Unknown',
            'errors': [f"Error loading file: {str(e)}"],
            'warnings': [],
            'suggestions': []
        }

def validate_all_lessons(lessons_dir: str = None) -> List[Dict[str, Any]]:
    """
    Validate all lesson files in the lessons directory
    
    Returns:
        List of validation results
    """
    if lessons_dir is None:
        lessons_dir = os.path.join(APP_DIR, 'data', 'lessons')
    
    results = []
    
    if not os.path.exists(lessons_dir):
        print(f"❌ Lessons directory not found: {lessons_dir}")
        return results
    
    lesson_files = [f for f in os.listdir(lessons_dir) if f.endswith('.json')]
    
    if not lesson_files:
        print(f"ℹ️ No lesson files found in {lessons_dir}")
        return results
    
    for filename in lesson_files:
        file_path = os.path.join(lessons_dir, filename)
        result = validate_lesson_file(file_path)
        results.append(result)
    
    return results

def print_validation_report(results: List[Dict[str, Any]]):
    """Print a comprehensive validation report"""
    
    print("📋 LESSON STRUCTURE VALIDATION REPORT")
    print("=" * 60)
    
    total_lessons = len(results)
    valid_lessons = sum(1 for r in results if r['valid'])
    invalid_lessons = total_lessons - valid_lessons
    
    print(f"📊 Summary: {valid_lessons}/{total_lessons} lessons valid")
    if invalid_lessons > 0:
        print(f"❌ {invalid_lessons} lessons have structural issues")
    else:
        print("✅ All lessons pass validation!")
    
    print("\n" + "=" * 60)
    
    for result in results:
        status = "✅" if result['valid'] else "❌"
        print(f"\n{status} {result['lesson_id']} - {result['title']}")
        print(f"   📁 {os.path.basename(result['file'])}")
        
        if result['errors']:
            print("   🚨 ERRORS:")
            for error in result['errors']:
                print(f"      • {error}")
        
        if result['warnings']:
            print("   ⚠️ WARNINGS:")
            for warning in result['warnings']:
                print(f"      • {warning}")
        
        if result['suggestions']:
            print("   💡 SUGGESTIONS:")
            for suggestion in result['suggestions']:
                print(f"      • {suggestion}")
    
    print("\n" + "=" * 60)
    
    # Summary recommendations
    if invalid_lessons > 0:
        print("\n🔧 RECOMMENDED ACTIONS:")
        print("1. Fix all structural errors marked above")
        print("2. Consider implementing suggested improvements")
        print("3. Re-run validation after changes")
        print("4. Update lesson loading system to handle new structure")

def migrate_lesson_file(file_path: str, backup: bool = True) -> bool:
    """
    Migrate a single lesson file to standard structure
    
    Returns:
        True if migration successful, False otherwise
    """
    try:
        # Load original
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Create backup if requested
        if backup:
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(original_data, f, indent=2, ensure_ascii=False)
            print(f"📁 Backup created: {backup_path}")
        
        # Migrate
        migrator = LessonMigrator()
        migrated_data = migrator.migrate_lesson(original_data)
        
        # Save migrated version
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(migrated_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migrated: {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed for {file_path}: {str(e)}")
        return False

def main():
    """Main function to run validation and migration"""
    
    print("🎓 LESSON STRUCTURE STANDARDIZATION TOOL")
    print("=" * 50)
    
    # Run validation
    print("\n🔍 Running validation...")
    results = validate_all_lessons()
    
    if not results:
        print("❌ No lesson files found to validate!")
        return
    
    # Print report
    print_validation_report(results)
    
    # Check if any lessons need migration
    needs_migration = [r for r in results if not r['valid']]
    
    if needs_migration:
        print(f"\n🔧 Found {len(needs_migration)} lessons that may benefit from migration")
        
        response = input("\nWould you like to attempt automatic migration? (y/n): ").lower().strip()
        
        if response == 'y':
            print("\n🚀 Starting migration...")
            
            for result in needs_migration:
                migrate_lesson_file(result['file'])
            
            print("\n🔄 Re-running validation after migration...")
            new_results = validate_all_lessons()
            print_validation_report(new_results)
        else:
            print("\n💡 Migration skipped. You can run migration manually later.")
    
    print("\n✨ Validation complete!")

if __name__ == "__main__":
    main()
