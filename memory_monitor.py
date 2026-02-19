import psutil
import os

def get_memory_usage():
    """
    Get current system memory usage percentage
    
    Returns:
        float: Memory usage percentage (0-100)
    """
    memory = psutil.virtual_memory()
    return memory.percent

def get_top_processes(n=3):
    """
    Get top N processes by memory usage
    
    Args:
        n (int): Number of top processes to return (default: 3)
    
    Returns:
        list: List of dictionaries containing process info
    """
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            # Get process info and filter out processes with None memory_percent
            proc_info = proc.info
            if proc_info['memory_percent'] is not None:
                processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes that no longer exist or we can't access
            continue
    
    # Sort by memory percentage in descending order
    processes.sort(key=lambda x: x['memory_percent'], reverse=True)
    
    return processes[:n]

def display_memory_info():
    """
    Display detailed memory information
    """
    try:
        memory = psutil.virtual_memory()
        print("\n" + "="*50)
        print("সিস্টেম মেমোরি তথ্য:")
        print("="*50)
        print(f"মোট মেমোরি: {memory.total / (1024**3):.2f} GB")
        print(f"ব্যবহৃত মেমোরি: {memory.used / (1024**3):.2f} GB")
        print(f"মুক্ত মেমোরি: {memory.available / (1024**3):.2f} GB")
        print(f"মেমোরি ব্যবহার: {memory.percent:.1f}%")
        print("="*50)
    except Exception as e:
        print(f"মেমোরি তথ্য লোড করতে সমস্যা: {e}")

def main():
    """
    Main function to check memory usage and display results
    """
    try:
        print("সিস্টেম মেমোরি মনিটর চালু করা হচ্ছে...\n")
        
        # Get current memory usage
        usage = get_memory_usage()
        print(f"সিস্টেম মেমোরি ব্যবহার: {usage:.1f}%")
        
        # Display detailed memory info
        display_memory_info()
        
        # Check if memory usage is high
        if usage > 80:
            print("\n⚠️  সতর্কতা: মেমোরি ব্যবহার ৮০% এর বেশি!")
            print("শীর্ষ ৩ মেমোরি ব্যবহারকারী প্রসেস:")
            print("-"*50)
            
            top_procs = get_top_processes()
            
            if not top_procs:
                print("কোনো প্রসেস তথ্য পাওয়া যায়নি।")
            else:
                for i, proc in enumerate(top_procs, 1):
                    print(f"{i}. PID: {proc['pid']}")
                    print(f"   নাম: {proc['name']}")
                    print(f"   মেমোরি ব্যবহার: {proc['memory_percent']:.1f}%")
                    print("-"*30)
            
            print("\n💡 পরামর্শ: কিছু অপ্রয়োজনীয় অ্যাপ্লিকেশন বন্ধ করুন অথবা মেমোরি অপ্টিমাইজ করুন।")
        
        elif usage > 60:
            print(f"\nℹ️  মেমোরি ব্যবহার মাঝারি পর্যায়ে ({usage:.1f}%)")
            print("সিস্টেম স্বাভাবিকভাবে চলছে, তবে মনিটরিং চালিয়ে যান।")
        
        else:
            print(f"\n✅ মেমোরি ব্যবহার স্বাভাবিক রয়েছে ({usage:.1f}%)")
            print("সিস্টেম ভালোভাবে কাজ করছে।")
        
        # Optional: Show swap memory info
        try:
            swap = psutil.swap_memory()
            if swap.total > 0:
                print(f"\nসোয়াপ মেমোরি: {swap.percent:.1f}% ব্যবহৃত")
        except:
            pass
            
    except ImportError:
        print("ত্রুটি: 'psutil' লাইব্রেরি ইনস্টল করা নেই।")
        print("ইনস্টল করতে চালান: pip install psutil")
        
    except PermissionError:
        print("ত্রুটি: এই স্ক্রিপ্টটি চালানোর জন্য পর্যাপ্ত অনুমতি নেই।")
        print("অ্যাডমিনিস্ট্রেটর হিসেবে চালানোর চেষ্টা করুন।")
        
    except Exception as e:
        print(f"অপ্রত্যাশিত ত্রুটি: {e}")
        print("দয়া করে আবার চেষ্টা করুন অথবা সিস্টেম অ্যাডমিনিস্ট্রেটরের সাথে যোগাযোগ করুন।")

if __name__ == "__main__":
    main()