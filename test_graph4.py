import matplotlib.pyplot as plt
from collections import Counter

def middle_square(seed, n_digits=4):
    """
    Generate a random number using the middle-square method.
    """
    squared = seed ** 2
    squared_str = str(squared).zfill(2 * n_digits)
    start = (len(squared_str) - n_digits) // 2
    middle = squared_str[start:start + n_digits]
    return int(middle)

def generate_sequence(initial_seed, n_iterations=500000, n_digits=4):
    """
    Generate a sequence of 500,000 numbers using middle-square method.
    """
    sequence = []
    seed = initial_seed
    seen = set()
    
    print(f"Generating {n_iterations:,} numbers...")
    
    for i in range(n_iterations):
        sequence.append(seed)
        seen.add(seed)
        
        next_seed = middle_square(seed, n_digits)
        
        if next_seed in seen or next_seed == 0:
            # If cycle detected, continue with a modified seed
            next_seed = (seed * 7 + 13) % (10 ** n_digits)
            
        seed = next_seed
        
        # Progress indicator
        if (i + 1) % 50000 == 0:
            print(f"Generated {i + 1:,}/{n_iterations:,} numbers...")
    
    return sequence

def plot_generated_numbers(sequence, initial_seed, show_every=100):
    """
    Create a line graph showing the generated numbers over time.
    
    Parameters:
    - sequence: list of generated numbers
    - initial_seed: starting seed value
    - show_every: plot every Nth number to avoid overcrowding (default 100 for 500k numbers)
    """
    fig, ax1 = plt.subplots(figsize=(18, 9))
    
    # Sample the sequence to avoid overcrowding
    sampled_indices = list(range(0, len(sequence), show_every))
    sampled_numbers = [sequence[i] for i in sampled_indices]
    
    # Create the main line plot
    color = 'tab:blue'
    ax1.set_xlabel('Iteration Number', fontsize=12)
    ax1.set_ylabel('Generated Number', fontsize=12, color=color)
    
    # Plot with markers for sampled points
    ax1.plot(sampled_indices, sampled_numbers, 
             marker='.', markersize=1, linewidth=0.8, 
             color=color, alpha=0.6, label=f'Generated Number (every {show_every}th)')
    
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Add a trend line (moving average) to show patterns
    window_size = 1000
    moving_avg = []
    
    print("Calculating moving average...")
    for i in range(0, len(sequence), show_every):
        start_idx = max(0, i - window_size)
        window = sequence[start_idx:i + 1]
        moving_avg.append(sum(window) / len(window))
    
    # Plot moving average
    ax1.plot(sampled_indices, moving_avg, 
             color='red', linewidth=2, linestyle='--', 
             alpha=0.8, label=f'Moving Average (window={window_size:,})')
    
    # Highlight cycle patterns
    ax2 = ax1.twinx()
    
    # Calculate frequency of each number in sliding windows
    window_size_freq = 5000
    unique_counts = []
    
    print("Calculating unique numbers in windows...")
    for i in sampled_indices:
        start_idx = max(0, i - window_size_freq)
        window = sequence[start_idx:i + 1]
        unique_counts.append(len(set(window)))
    
    color2 = 'tab:green'
    ax2.set_ylabel(f'Unique Numbers in Last {window_size_freq:,}', fontsize=12, color=color2)
    ax2.plot(sampled_indices, unique_counts, 
             marker='', markersize=0, linewidth=1.2, 
             color=color2, alpha=0.6, linestyle=':',
             label=f'Unique Numbers (window={window_size_freq:,})')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Format x-axis with comma separators
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Title and legend
    plt.title(f'Middle-Square Algorithm: Generated Numbers Over Time\n'
              f'Initial Seed: {initial_seed} | Total Numbers Generated: {len(sequence):,}', 
              fontsize=14, fontweight='bold')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.show()

def plot_sequence_distribution(sequence, initial_seed):
    """
    Create additional visualization showing the distribution of generated numbers.
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 11))
    
    # 1. Full sequence line plot (first 2000 numbers for clarity)
    ax1 = axes[0, 0]
    first_2000 = sequence[:2000]
    ax1.plot(range(len(first_2000)), first_2000, 
             linewidth=0.8, color='navy', alpha=0.8)
    ax1.set_xlabel('Iteration Number', fontsize=11)
    ax1.set_ylabel('Generated Number', fontsize=11)
    ax1.set_title('First 2,000 Generated Numbers', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # 2. Histogram of all generated numbers
    ax2 = axes[0, 1]
    ax2.hist(sequence, bins=100, color='steelblue', edgecolor='black', alpha=0.7, linewidth=0.5)
    ax2.set_xlabel('Generated Number', fontsize=11)
    ax2.set_ylabel('Frequency', fontsize=11)
    ax2.set_title('Distribution of All 500,000 Generated Numbers', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # 3. Scatter plot showing patterns (sampled)
    ax3 = axes[1, 0]
    sample_size = 10000
    x_vals = sequence[:sample_size-1]
    y_vals = sequence[1:sample_size]
    ax3.scatter(x_vals, y_vals, 
                c=range(len(x_vals)), cmap='viridis', 
                alpha=0.3, s=1)
    ax3.set_xlabel('Current Number', fontsize=11)
    ax3.set_ylabel('Next Number', fontsize=11)
    ax3.set_title(f'Number Transitions (First {sample_size:,} points)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # 4. Sequence over time with zoom (last 5000 numbers)
    ax4 = axes[1, 1]
    last_5000 = sequence[-5000:]
    ax4.plot(range(len(last_5000)), last_5000, 
             linewidth=0.8, color='darkred', alpha=0.8)
    ax4.set_xlabel('Iteration Number (relative)', fontsize=11)
    ax4.set_ylabel('Generated Number', fontsize=11)
    ax4.set_title(f'Last 5,000 Generated Numbers (of {len(sequence):,})', fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f'Middle-Square Algorithm Analysis - Initial Seed: {initial_seed} | Total: {len(sequence):,} numbers', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.show()

def print_sequence_sample(sequence, sample_size=30):
    """
    Print a sample of the generated sequence.
    """
    print("\n" + "="*70)
    print(f"SAMPLE OF GENERATED SEQUENCE (First {sample_size} numbers):")
    print("="*70)
    for i in range(0, min(sample_size, len(sequence)), 10):
        row = sequence[i:i+10]
        print(f"  {i+1:6,}-{i+10:6,}: {row}")
    
    print("\n" + "="*70)
    print(f"LAST {sample_size} NUMBERS:")
    print("="*70)
    start_idx = len(sequence) - sample_size
    for i in range(start_idx, len(sequence), 10):
        end_idx = min(i+10, len(sequence))
        row = sequence[i:end_idx]
        print(f"  {i+1:6,}-{end_idx:6,}: {row}")

def detect_cycles(sequence, max_cycle_length=10000):
    """
    Detect and report any cycles in the sequence.
    """
    print("\n" + "="*70)
    print("CYCLE DETECTION")
    print("="*70)
    
    # Look for repeating patterns
    seen_sequences = {}
    
    for cycle_len in [10, 20, 50, 100, 200, 500, 1000]:
        # Check last portion of sequence for cycles
        check_start = len(sequence) - cycle_len * 10
        if check_start < 0:
            check_start = 0
            
        for i in range(check_start, len(sequence) - cycle_len):
            pattern = tuple(sequence[i:i+cycle_len])
            if pattern in seen_sequences:
                print(f"Possible cycle of length {cycle_len} detected at position {i:,}")
                print(f"  Pattern starts with: {list(pattern[:10])}...")
                break
            seen_sequences[pattern] = i
        else:
            print(f"No cycle of length {cycle_len} detected in checked range")
        
        seen_sequences.clear()

def main():
    """
    Main function to run the middle-square algorithm and visualize results.
    """
    # Parameters
    INITIAL_SEED = 1234
    TOTAL_NUMBERS = 500000
    N_DIGITS = 4
    SHOW_EVERY = 500  # Show every 500th number in the main plot (1000 points total)
    
    print("="*70)
    print("MIDDLE-SQUARE ALGORITHM - VON NEUMANN (1949)")
    print("="*70)
    print(f"Initial Seed: {INITIAL_SEED}")
    print(f"Total Numbers to Generate: {TOTAL_NUMBERS:,}")
    print(f"Digit Length: {N_DIGITS}")
    print("="*70)
    
    # Generate sequence of 500,000 numbers
    sequence = generate_sequence(INITIAL_SEED, TOTAL_NUMBERS, N_DIGITS)
    
    print(f"\nGeneration complete! Total numbers: {len(sequence):,}")
    
    # Print sample of the sequence
    print_sequence_sample(sequence, 30)
    
    # Print statistics
    print("\n" + "="*70)
    print("SEQUENCE STATISTICS")
    print("="*70)
    print(f"Total numbers generated: {len(sequence):,}")
    print(f"Unique numbers: {len(set(sequence)):,}")
    print(f"Minimum value: {min(sequence)}")
    print(f"Maximum value: {max(sequence)}")
    print(f"Average value: {sum(sequence)/len(sequence):.2f}")
    
    # Most common numbers overall
    counter = Counter(sequence)
    print(f"\nTop 15 most frequent numbers:")
    for num, count in counter.most_common(15):
        percentage = (count / len(sequence)) * 100
        print(f"  {num:4d}: {count:6,} times ({percentage:6.3f}%)")
    
    # Detect cycles
    detect_cycles(sequence)
    
    # Create the main visualization showing generated numbers
    print("\nCreating main visualization...")
    plot_generated_numbers(sequence, INITIAL_SEED, SHOW_EVERY)
    
    # Create detailed distribution plots
    print("Creating distribution plots...")
    plot_sequence_distribution(sequence, INITIAL_SEED)
    
    print("\nAnalysis complete! Check the plots for visualizations.")

if __name__ == "__main__":
    main()