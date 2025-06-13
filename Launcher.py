import subprocess
import sys
import os

def run_script(script_name):
    """Execute a file python"""
    try:
        print(f"🚀 Launching {script_name}...")
        print("-" * 50)
        
        # Check if script exists
        if not os.path.exists(script_name):
            print(f"❌ Error: {script_name} not found!")
            return False
        
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully!")
            return True
        else:
            print(f"❌ {script_name} failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error executing {script_name}: {e}")
        return False

def main():
    """Launch both scripts sequentially"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🔄 Starting CSV Processing and AutoCAD Script Generation Pipeline...")
    print("=" * 70)
    print(f"📁 Working directory: {script_dir}")
    print("=" * 70)
    
    # Step 1: Run CSV filter script
    print("\n📊 STEP 1: CSV Filtering and Sorting")
    success1 = run_script("Filter_file_csv.py")
    
    if success1:
        print("\n" + "=" * 70)
        print("📝 STEP 2: AutoCAD Script Generation")
        
        # Step 2: Run AutoCAD script generation
        success2 = run_script("Generate_file_scr.py")
        
        if success2:
            print("\n" + "=" * 70)
            print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print("✅ CSV data has been filtered and sorted")
            print("✅ AutoCAD script has been generated")
            print("📁 Check your Output_folder for the final script")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("⚠️ PIPELINE PARTIALLY COMPLETED")
            print("✅ CSV filtering completed successfully")
            print("❌ AutoCAD script generation failed")
            print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("🛑 PIPELINE STOPPED")
        print("❌ CSV filtering failed - AutoCAD script generation skipped")
        print("=" * 70)

if __name__ == "__main__":
    main()
