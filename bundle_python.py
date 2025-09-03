# Build script to bundle Python source files for web deployment
import os
import shutil
from pathlib import Path

def bundle_python_package():
    """Bundle the pqtorus Python package for web deployment"""
    
    # Source and destination paths
    python_src = Path(__file__).parent / "python" / "src" / "pqtorus"
    web_assets = Path(__file__).parent / "web" / "public" / "python"
    
    # Create destination directory
    web_assets.mkdir(parents=True, exist_ok=True)
    
    # Copy Python source files
    if python_src.exists():
        # Clean destination
        if (web_assets / "pqtorus").exists():
            shutil.rmtree(web_assets / "pqtorus")
        
        # Copy package
        shutil.copytree(python_src, web_assets / "pqtorus")
        print(f"Copied Python package from {python_src} to {web_assets / 'pqtorus'}")
        
        # Create a combined package file for easier loading
        combined_code = []
        
        # Read all Python files and combine them
        for py_file in python_src.glob("*.py"):
            if py_file.name != "__init__.py":
                with open(py_file, 'r') as f:
                    combined_code.append(f"# From {py_file.name}\n")
                    combined_code.append(f.read())
                    combined_code.append("\n\n")
        
        # Write combined file
        with open(web_assets / "pqtorus_combined.py", 'w') as f:
            f.write("".join(combined_code))
        
        print(f"Created combined package file: {web_assets / 'pqtorus_combined.py'}")
    else:
        print(f"Python source directory not found: {python_src}")

if __name__ == "__main__":
    bundle_python_package()