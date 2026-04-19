import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def middle_square(seed, n_digits=4):
    """
    Generate a random number using the middle-square method.
    
    Parameters:
    seed: initial seed value
    n_digits: number of digits to use (default 4)
    
    Returns:
    next random number in the sequence
    """
    # Square the seed
    squared = seed ** 2
    
    # Convert to string to extract middle digits
    squared_str = str(squared).zfill(2 * n_digits)
    
    # Calculate start position for middle digits
    start = (len(squared_str) - n_digits) // 2
    
    # Extract middle digits
    middle = squared_str[start:start + n_digits]
    
    return int(middle)

def generate_sequence(initial_seed, n_iterations=1000, n_digits=4):
    """
    Generate a sequence of random numbers using the middle-square method.
    
    Parameters:
    initial_seed: starting seed value
    n_iterations: number of random numbers to generate
    n_digits: number of digits for the middle-square algorithm
    
    Returns:
    list of generated numbers
    """
    sequence = []
    seed = initial_seed
    seen = set()
    
    for _ in range(n_iterations):
        sequence.append(seed)
        seen.add(seed)
        
        # Generate next number
        next_seed = middle_square(seed, n_digits)
        
        # Check for degeneration (stuck in zero or repeating cycle)
        if next_seed in seen:
            print(f"Cycle detected at iteration {len(sequence)}")
            break
            
        seed = next_seed
    
    return sequence

def count_frequencies_over_time(sequence, window_size=50):
    """
    Track the frequency counts of numbers over time.
    
    Parameters:
    sequence: list of generated numbers
    window_size: size of sliding window for frequency analysis
    
    Returns:
    dict with time series of frequencies for each number
    """
    frequency_history = {}
    
    for i in range(1, len(sequence) + 1):
        # Get current window
        window = sequence[max(0, i - window_size):i]
        
        # Count frequencies in current window
        counter = Counter(window)
        
        # Store frequencies for each number
        for num, count in counter.items():
            if num not in frequency_history:
                frequency_history[num] = []
            frequency_history[num].append(count)
    
    return frequency_history

def plot_frequency_distribution(sequence, window_size=100, top_n=10):
    """
    Create a line plot showing the frequency of the most common numbers over time.
    
    Parameters:
    sequence: list of generated numbers
    window_size: size of sliding window for frequency analysis
    top_n: number of most frequent numbers to display
    """
    # Count frequencies over time
    freq_history = count_frequencies_over_time(sequence, window_size)
    
    # Find the most frequently occurring numbers overall
    overall_counter = Counter(sequence)
    most_common = [num for num, _ in overall_counter.most_common(top_n)]
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    colors = plt.cm.tab10(np.linspace(0, 1, top_n))
    
    for i, num in enumerate(most_common):
        if num in freq_history:
            frequencies = freq_history[num]
            time_points = list(range(1, len(frequencies) + 1))
            plt.plot(time_points, frequencies, 
                    label=f'Number {num}', 
                    color=colors[i], 
                    linewidth=2,
                    alpha=0.8)
    
    plt.xlabel('Iteration Number', fontsize=12)
    plt.ylabel(f'Frequency in Last {window_size} Numbers', fontsize=12)
    plt.title(f'Middle-Square Algorithm: Most Frequent Numbers Over Time\n'
              f'(Initial Seed: {sequence[0]}, Total Generated: {len(sequence)})', 
              fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    

def analyze_middle_square(initial_seed, n_iterations=1000, n_digits=4, top_n=10):
    """
    Complete analysis of the middle-square algorithm.
    
    Parameters:
    initial_seed: starting seed value
    n_iterations: number of iterations
    n_digits: number of digits for the algorithm
    top_n: number of top frequent numbers to plot
    """
    print(f"Middle-Square Algorithm Analysis")
    print(f"Initial Seed: {initial_seed}")
    print(f"Number of Digits: {n_digits}")
    print("-" * 50)
    
    # Generate sequence
    sequence = generate_sequence(initial_seed, n_iterations, n_digits)
    
    print(f"Generated {len(sequence)} numbers")
    print(f"Unique numbers: {len(set(sequence))}")
    
    # Show some statistics
    counter = Counter(sequence)
    print(f"\nTop 10 most frequent numbers:")
    for num, count in counter.most_common(10):
        percentage = (count / len(sequence)) * 100
        print(f"  {num}: {count} times ({percentage:.2f}%)")
    
    
    # Additional plot: Distribution histogram
    plt.figure(figsize=(12, 6))
    plt.hist(sequence, bins=min(50, len(set(sequence))), 
             alpha=0.7, edgecolor='black')
    plt.xlabel('Generated Number', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(f'Distribution of Generated Numbers\n(Initial Seed: {initial_seed}, {len(sequence)} iterations)', 
              fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return sequence


if __name__ == "__main__":
    # Test with a 4-digit seed (classic von Neumann example)
    print("Classic 4-digit implementation")
    sequence1 = analyze_middle_square(initial_seed=6753, n_iterations=500, n_digits=4, top_n=8)
    
   
    
   