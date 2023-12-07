import spacy
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import json
from typing import List, Dict, Callable
from langdetect import detect

class TranscriptProcessor:
    def __init__(self, transcript):

        self.transcript = transcript
        self.language = detect(''.join(element['text'] for element in transcript))
        self.nlp = self.load_spacy_model()
        self.sentences = self.get_sentences()  # List of sentences without timecodes
        self.sentences_with_timecodes = self.get_sentences_with_timecodes()  # List of sentences with timecodes 
        
    def load_spacy_model(self):
        """Map the detected language to the corresponding spaCy model."""
        
        # This dictionary can be expanded with more languages and their models
        spacy_models = {
            'en': 'en_core_web_sm',  # English
            'ko': 'ko_core_news_sm',  # Korean
            'ja': 'ja_core_news_sm',  # Japanese
            'es': 'es_core_news_sm',  # Spanish
            'pt': 'pt_core_news_sm',  # Portuguese
            # Add more as needed
        }
        # Load the spaCy model
        if self.language in spacy_models:
            model_name = spacy_models[self.language]
        else:
            model_name = 'xx_sent_ud_sm' # Multi-language model
        
        return spacy.load(model_name)

    def get_sentences(self):
        """Extract sentences from the transcript."""

        txt_formatter = TextFormatter()
        text_formatted = txt_formatter.format_transcript(self.transcript).replace("\n", " ")
        doc = self.nlp(text_formatted)

        return list(doc.sents)

    def get_sentences_with_timecodes(self):
        """Extract sentences with timecodes from the transcript."""

        txt_formatter = TextFormatter()
        text_formatted = txt_formatter.format_transcript(self.transcript).replace("\n", " ")
        doc = self.nlp(text_formatted)

        sentences_with_timecodes = []
        prev_end_time = None

        for sentence in doc.sents:
            start_time, end_time = None, None

            for entry in self.transcript:
                entry_text = entry["text"].replace("\n", " ")
                if start_time is None and entry_text in sentence.text:
                    start_time = entry["start"]
                if entry_text in sentence.text:
                    end_time = entry["start"] + entry["duration"]

            if start_time is None:
                start_time = prev_end_time

            sentences_with_timecodes.append(
                (
                    sentence.text,
                    start_time,
                    end_time if end_time is not None else prev_end_time,
                )
            )
            prev_end_time = end_time

        return sentences_with_timecodes

    @staticmethod
    def remove_quotations(text):
        """Remove both single and double quotes from the text."""
        return text.replace("'", "").replace('"', "")

    @staticmethod
    def jaccard_similarity(set1, set2):
        """Calculate the Jaccard Similarity between two sets."""
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union) if union else 0
    
    @staticmethod
    def convert_to_json(sentences_with_timecodes):
        """
        Convert a list of sentences with timecodes to a JSON string format.
        """
        json_output = []

        for index, (text, start, end) in enumerate(sentences_with_timecodes):
            sentence_info = {
                "id": index,
                "text": text,
                "start": start,
                "end": end,
            }
            json_output.append(sentence_info)

        return json.dumps(json_output, ensure_ascii=False, indent=4)
    
    @classmethod
    def find_sentence_by_subset(cls, input_sentence, json_data):
        """
        Find the index of a sentence in the list of dictionaries based on subset matching.
        """
        # Parse the JSON data back into a Python object
        sentence_list = json.loads(json_data)

        input_tokens = set(cls.remove_quotations(input_sentence).lower().split())

        for sentence_data in sentence_list:
            dict_tokens = set(cls.remove_quotations(sentence_data["text"]).lower().split())
            if input_tokens.issubset(dict_tokens) or dict_tokens.issubset(input_tokens):
                return sentence_data["id"]  # Returning the index of the sentence

        return None  # If no matching sentence is found

    @classmethod
    def find_sentence_by_similarity(cls, input_sentence, json_data, threshold=0.60):
        """
        Find the index of a sentence in the list of dictionaries based on a similarity threshold.
        """
        # Parse the JSON data back into a Python object
        sentence_list = json.loads(json_data)

        input_tokens = set(cls.remove_quotations(input_sentence).lower().split())

        for sentence_data in sentence_list:
            dict_tokens = set(cls.remove_quotations(sentence_data["text"]).lower().split())
            similarity = cls.jaccard_similarity(input_tokens, dict_tokens)
            if similarity >= threshold:
                return sentence_data["id"]  # Returning the index of the sentence

        return None  # If no sentence meets the threshold

    def process_chapters(self, output_SEG: str) -> List[Dict]:
        """
        Process chapters from a given JSON string and a list of sentences with timecodes, updating each chapter with subtitles and time intervals.
        """

        def find_index(method: Callable, default_method: Callable, line: str) -> int:
            """
            Finds the index of a sentence in the json_data using the given method,
            falls back to the default method if the first method returns None.

            Args:
            - method (Callable): The primary method to use for finding the index.
            - default_method (Callable): The fallback method if the primary method fails.
            - line (str): The sentence line to find in the json_data.

            Returns:
            - int: The index of the sentence in the json_data.
            """
            index = method(line, self.convert_to_json(self.sentences_with_timecodes))
            if index is None:
                index = default_method(line, self.convert_to_json(self.sentences_with_timecodes))
            return index

        # Load chapters from the JSON string
        chapters = json.loads(output_SEG)["chapters"]

        # Process each chapter
        for chapter in chapters:
            # Find start and end indexes of the chapter in sentences_with_timecodes
            start_index = find_index(
                self.find_sentence_by_subset,
                self.find_sentence_by_similarity,
                chapter["start_line"],
            )
            end_index = find_index(
                self.find_sentence_by_subset,
                self.find_sentence_by_similarity,
                chapter["end_line"],
            )
            print(start_index, end_index)
            # Construct the subtitle for the chapter
            chapter_subtitle = " ".join(
                [
                    sentence_with_timecode[0]
                    for sentence_with_timecode in self.sentences_with_timecodes[start_index : end_index + 1]
                ]
            )
            chapter["subtitle"] = chapter_subtitle

            # Set start and end times for the chapter
            chapter["start_time"] = self.sentences_with_timecodes[start_index][1]
            chapter["end_time"] = self.sentences_with_timecodes[end_index][2]

        return chapters


# Main execution
if __name__ == "__main__":
    partner_video_id = "t7tA3NNKF0Q"

    transcript_list = YouTubeTranscriptApi.list_transcripts(partner_video_id)

    # Finding the automatic transcript from the list
    for transcript in transcript_list:
        if not transcript.is_generated and "en" == transcript.language_code:
            target_language = transcript.language_code

    print(target_language)

    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[target_language])

    processor = TranscriptProcessor(transcript)
    print(processor.sentences)
