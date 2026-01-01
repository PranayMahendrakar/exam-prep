#!/usr/bin/env python3
"""
Exam Preparation Question Generator - Llama-Based Study Tool
Creates practice questions based on course materials
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json
from typing import List

console = Console()

QUESTION_TYPES = ["Multiple Choice", "True/False", "Short Answer", "Essay",
                  "Fill in the Blank", "Matching", "Problem Solving", "Case Analysis"]

BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]


class ExamQuestionGenerator:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.question_bank = []
        self.quiz_history = []
    
    def generate_questions(self, content: str, num_questions: int = 5, 
                          question_type: str = "Mixed", difficulty: str = "medium") -> dict:
        prompt = f"""Generate exam practice questions from this content.

Content:
{content}

Number of Questions: {num_questions}
Question Type: {question_type}
Difficulty: {difficulty}

Return JSON:
{{
    "topic": "main topic covered",
    "difficulty": "{difficulty}",
    "questions": [
        {{
            "id": 1,
            "type": "question type",
            "bloom_level": "cognitive level",
            "question": "question text",
            "options": ["A) option", "B) option", "C) option", "D) option"],
            "correct_answer": "A",
            "explanation": "why this is correct",
            "common_mistakes": ["wrong answers students pick"],
            "hint": "helpful hint",
            "points": 10
        }}
    ],
    "total_points": 50,
    "time_estimate": "minutes to complete",
    "study_tips": ["tips based on question topics"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        result = self._parse_json(response['message']['content'])
        self.question_bank.extend(result.get('questions', []))
        return result
    
    def generate_by_bloom(self, topic: str, bloom_level: str) -> dict:
        prompt = f"""Generate questions at {bloom_level} cognitive level for this topic.

Topic: {topic}
Bloom's Level: {bloom_level}

Return JSON:
{{
    "topic": "{topic}",
    "bloom_level": "{bloom_level}",
    "level_description": "what this level tests",
    "action_verbs": ["verbs used at this level"],
    "questions": [
        {{
            "id": 1,
            "question": "question testing {bloom_level}",
            "type": "appropriate question type",
            "answer_key": "expected answer",
            "grading_rubric": "how to evaluate",
            "sample_excellent_answer": "what a great answer looks like"
        }}
    ],
    "progression": {{
        "prerequisite_level": "level before this",
        "next_level": "level after this",
        "how_to_upgrade": "how to make question harder"
    }}
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def create_practice_exam(self, topics: List[str], duration_minutes: int = 60) -> dict:
        prompt = f"""Create a practice exam.

Topics: {json.dumps(topics)}
Duration: {duration_minutes} minutes

Return JSON:
{{
    "exam_info": {{
        "title": "Practice Exam",
        "topics_covered": {json.dumps(topics)},
        "total_time": "{duration_minutes} minutes",
        "total_points": 100
    }},
    "instructions": "exam instructions",
    "sections": [
        {{
            "section": "Section A: Multiple Choice",
            "points": 30,
            "time_allocation": "15 minutes",
            "questions": [
                {{
                    "number": 1,
                    "question": "question text",
                    "options": ["A)", "B)", "C)", "D)"],
                    "points": 5,
                    "answer": "A",
                    "topic": "which topic"
                }}
            ]
        }}
    ],
    "answer_key": [
        {{
            "question": 1,
            "answer": "A",
            "explanation": "why"
        }}
    ],
    "grading_scale": {{
        "A": "90-100",
        "B": "80-89",
        "C": "70-79",
        "D": "60-69",
        "F": "below 60"
    }},
    "study_recommendations": ["based on exam content"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        result = self._parse_json(response['message']['content'])
        self.quiz_history.append(result)
        return result
    
    def generate_flashcards(self, content: str, num_cards: int = 10) -> dict:
        prompt = f"""Generate study flashcards from this content.

Content:
{content}

Number of Cards: {num_cards}

Return JSON:
{{
    "topic": "main topic",
    "flashcards": [
        {{
            "id": 1,
            "front": "question/term/prompt",
            "back": "answer/definition/explanation",
            "category": "subtopic",
            "difficulty": "easy/medium/hard",
            "memory_tip": "how to remember"
        }}
    ],
    "study_suggestions": {{
        "spaced_repetition": "recommended schedule",
        "grouping": "how to organize cards",
        "review_order": "suggested sequence"
    }}
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def check_answer(self, question: str, student_answer: str, correct_answer: str) -> dict:
        prompt = f"""Evaluate this student answer.

Question: {question}
Student's Answer: {student_answer}
Expected Answer: {correct_answer}

Return JSON:
{{
    "question": "{question}",
    "student_answer": "{student_answer}",
    "correct_answer": "{correct_answer}",
    "evaluation": {{
        "is_correct": true,
        "score": 85,
        "max_score": 100
    }},
    "feedback": {{
        "strengths": ["what's good"],
        "weaknesses": ["what's missing"],
        "misconceptions": ["any misunderstandings"],
        "specific_corrections": ["what to fix"]
    }},
    "improved_answer": "how to write a better answer",
    "related_concepts": ["concepts to review"],
    "encouragement": "motivational feedback"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="📝 Exam Preparation Question Generator", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Generate Questions", "Create from content")
    table.add_row("2", "Bloom's Taxonomy", "Questions by level")
    table.add_row("3", "Practice Exam", "Full practice test")
    table.add_row("4", "Flashcards", "Generate flashcards")
    table.add_row("5", "Check Answer", "Evaluate your answer")
    table.add_row("6", "View Bank", "See saved questions")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]📝 Exam Preparation Question Generator[/bold blue]\n"
        "[green]AI-Powered Practice Question Creation[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    generator = ExamQuestionGenerator()
    
    while True:
        display_menu()
        console.print(f"[dim]Question Bank: {len(generator.question_bank)} questions[/dim]")
        
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Ace that exam! 📝[/yellow]")
            break
        
        elif choice == "6":
            if generator.question_bank:
                for i, q in enumerate(generator.question_bank[-5:], 1):
                    console.print(f"  {i}: {q.get('question', 'N/A')[:60]}...")
            else:
                console.print("[dim]No questions in bank.[/dim]")
            continue
        
        with console.status("[bold green]Generating questions..."):
            if choice == "1":
                console.print("[dim]Paste study content (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                num = IntPrompt.ask("Number of questions", default=5)
                qtype = Prompt.ask("Question type", default="Mixed")
                difficulty = Prompt.ask("Difficulty", choices=["easy", "medium", "hard"], default="medium")
                result = generator.generate_questions("\n".join(lines), num, qtype, difficulty)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="❓ Generated Questions"))
            
            elif choice == "2":
                topic = Prompt.ask("Topic")
                console.print(f"\n[bold]Bloom's Levels:[/bold] {', '.join(BLOOM_LEVELS)}")
                level = Prompt.ask("Bloom's level", default="Apply")
                result = generator.generate_by_bloom(topic, level)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title=f"🎯 {level} Level Questions"))
            
            elif choice == "3":
                topics = Prompt.ask("Topics (comma-separated)").split(",")
                duration = IntPrompt.ask("Duration (minutes)", default=60)
                result = generator.create_practice_exam([t.strip() for t in topics], duration)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📋 Practice Exam"))
            
            elif choice == "4":
                console.print("[dim]Paste content (end with 'EOF'):[/dim]")
                lines = []
                while True:
                    line = input()
                    if line.strip() == "EOF":
                        break
                    lines.append(line)
                num = IntPrompt.ask("Number of flashcards", default=10)
                result = generator.generate_flashcards("\n".join(lines), num)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="🗂️ Flashcards"))
            
            elif choice == "5":
                question = Prompt.ask("Question")
                student_answer = Prompt.ask("Your answer")
                correct = Prompt.ask("Correct answer")
                result = generator.check_answer(question, student_answer, correct)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="✓ Answer Evaluation"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
