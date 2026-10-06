import spacy
import re
from typing import Dict, List, Any
import json

class NLPPipeline:
    def __init__(self):
        # Load spaCy model (you might need to install: python -m spacy download en_core_web_sm)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None

        # Intent patterns (simple rule-based for demo)
        self.intent_patterns = {
            "admission_info": [
                "admission", "apply", "application", "eligibility", "entrance",
                "how to apply", "admission process", "requirements"
            ],
            "course_info": [
                "course", "program", "syllabus", "curriculum", "degree",
                "engineering", "science", "commerce", "subjects"
            ],
            "fee_inquiry": [
                "fee", "cost", "tuition", "payment", "scholarship",
                "how much", "price", "charges", "financial"
            ],
            "hostel_info": [
                "hostel", "accommodation", "room", "boarding", "residence",
                "stay", "facilities", "mess"
            ],
            "library_info": [
                "library", "book", "study", "reading", "resources",
                "digital", "journal", "database"
            ],
            "placement_info": [
                "placement", "job", "career", "internship", "recruitment",
                "companies", "salary", "campus hiring"
            ],
            "contact_info": [
                "contact", "phone", "email", "address", "location",
                "office", "department", "reach"
            ],
            "general_info": [
                "about", "college", "university", "campus", "facilities",
                "history", "achievements"
            ]
        }

    def process(self, text: str) -> Dict[str, Any]:
        """Process input text and extract intent and entities"""

        # Clean and preprocess text
        cleaned_text = self._clean_text(text)

        # Extract intent
        intent = self._extract_intent(cleaned_text)

        # Extract entities
        entities = self._extract_entities(cleaned_text)

        # Calculate confidence (simple heuristic)
        confidence = self._calculate_confidence(cleaned_text, intent)

        return {
            "intent": intent,
            "entities": entities,
            "confidence": confidence,
            "processed_text": cleaned_text
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        # Convert to lowercase
        text = text.lower().strip()

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters except basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)

        return text

    def _extract_intent(self, text: str) -> str:
        """Extract intent from text using pattern matching"""
        text_lower = text.lower()

        intent_scores = {}

        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in text_lower:
                    # Give higher score for exact matches
                    score += 2 if pattern == text_lower else 1

            if score > 0:
                intent_scores[intent] = score

        if intent_scores:
            # Return intent with highest score
            return max(intent_scores, key=intent_scores.get)
        else:
            return "general_info"

    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract entities from text"""
        entities = []

        if self.nlp is None:
            return entities

        doc = self.nlp(text)

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "description": spacy.explain(ent.label_) or ent.label_
            })

        # Extract custom entities specific to college domain
        college_entities = self._extract_college_entities(text)
        entities.extend(college_entities)

        return entities

    def _extract_college_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract college-specific entities"""
        entities = []
        text_lower = text.lower()

        # Course names
        courses = ["engineering", "science", "commerce", "bba", "mba", "btech", "mtech"]
        for course in courses:
            if course in text_lower:
                entities.append({
                    "text": course,
                    "label": "COURSE",
                    "description": "Academic course or program"
                })

        # Departments
        departments = ["computer science", "electronics", "mechanical", "civil", "physics", "chemistry"]
        for dept in departments:
            if dept in text_lower:
                entities.append({
                    "text": dept,
                    "label": "DEPARTMENT",
                    "description": "Academic department"
                })

        return entities

    def _calculate_confidence(self, text: str, intent: str) -> float:
        """Calculate confidence score for intent detection"""
        if intent == "general_info":
            return 0.5  # Low confidence for fallback intent

        patterns = self.intent_patterns.get(intent, [])
        matches = sum(1 for pattern in patterns if pattern in text.lower())

        # Simple confidence calculation
        confidence = min(0.9, matches / len(patterns) + 0.3)
        return round(confidence, 2)
