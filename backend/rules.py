import re
from typing import Dict, Any

def check_signatures(text: str) -> bool:
    """
    Check if the document has a signature block.
    Looks for common patterns like 'Signed by', 'Signature', 'Authorized signatory'.
    """
    patterns = [
        r"signed by", 
        r"signature", 
        r"authori[sz]ed signatory", 
        r"witness"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_dates(text: str) -> bool:
    """
    Check if the document contains at least one valid date.
    """
    date_patterns = [
        r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b",   # 01-01-2024, 01/01/24
        r"\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b",     # 2024-01-01
        r"\b(january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\s+\d{1,2},?\s+\d{4}\b"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in date_patterns)


def check_parties(text: str) -> bool:
    """
    Look for contract parties (e.g., 'between X and Y').
    """
    patterns = [
        r"between\s+.+?\s+and\s+.+",  # Between Party A and Party B
        r"this agreement is made.*?by and between", 
        r"party\s+[ab]"
    ]
    return any(re.search(p, text, re.IGNORECASE | re.DOTALL) for p in patterns)


def check_jurisdiction(text: str) -> bool:
    """
    Look for governing law/jurisdiction clauses.
    """
    patterns = [
        r"governed by the laws of\s+.+", 
        r"jurisdiction of\s+.+", 
        r"courts of\s+.+"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def run_rule_checks(text: str) -> Dict[str, Any]:
    """
    Run all rule-based checks on the document text.
    Returns a dictionary with pass/fail for each rule.
    """
    return {
        "signatures": check_signatures(text),
        "dates": check_dates(text),
        "parties": check_parties(text),
        "jurisdiction": check_jurisdiction(text)
    }
