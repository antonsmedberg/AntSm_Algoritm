from collections import Counter
from itertools import islice
from typing import List, Optional, Union, Callable, Iterable

SequenceType = Union[str, Iterable]  # Utökat stöd för fler itererbara typer
IndexPair = tuple[int, int]  # Tydligare typdefinition

def is_unique_window(element_counts: Counter, window_size: int) -> bool:
    """Kontrollerar om alla element i fönstret är unika."""
    return sum(count == 1 for count in element_counts.values()) == window_size

def update_window_counts(element_counts: Counter, exiting: Optional[str], entering: str) -> None:
    """Optimerad uppdatering av Counter för element som lämnar och träder in i fönstret."""
    if exiting:
        element_counts[exiting] -= 1
        if element_counts[exiting] == 0:
            del element_counts[exiting]
    element_counts[entering] += 1

def find_unique_sequences_optimized(
    sequence: SequenceType,
    window_sizes: Union[int, List[int]],  # Ändrad för att stödja en lista av storlekar
    find_all: bool = False,
    ignore_case: bool = False,
    custom_comparison: Optional[Callable[[str], str]] = None
) -> Optional[List[IndexPair]]:
    """
    Förbättrad dokumentation med tydligare beskrivning och fler exempel.
    
    Ny funktionalitet: Stödjer nu negativ window_size och en lista av window_sizes för flexibilitet.
    """
    
    if isinstance(sequence, str) and ignore_case:
        sequence = sequence.lower()
    elif custom_comparison:
        sequence = map(custom_comparison, sequence)

    sequence = list(sequence)  # Konverterar till lista för flexibel indexering
    unique_sequences = []

    window_sizes = [window_sizes] if isinstance(window_sizes, int) else window_sizes
    for window_size in window_sizes:
        if window_size < 0:  # Hanterar negativ window_size
            window_size = len(sequence) + window_size + 1
        if not 1 <= window_size <= len(sequence):
            raise ValueError(f"Window size {window_size} is out of valid range for the sequence length.")

        element_counts = Counter(islice(sequence, 0, window_size))
        if is_unique_window(element_counts, window_size):
            unique_sequences.append((0, window_size - 1))

        for i in range(1, len(sequence) - window_size + 1):
            exiting = sequence[i - 1]
            entering = sequence[i + window_size - 1]
            update_window_counts(element_counts, exiting, entering)

            if is_unique_window(element_counts, window_size):
                unique_sequences.append((i, i + window_size - 1))
                if not find_all:
                    break

    return unique_sequences








