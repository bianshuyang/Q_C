import os
import timeit
import subprocess
import heapq

def main():
    # Ask for a filename
    filename = "main"

    # Define the input directory
    input_dir = "./secret"

    # List all the .in files in the directory
    input_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.in')]

    # Determine the file extension and choose the appropriate run command
    if os.path.isfile(f"{filename}.py"):
        command = f"python {filename}.py"
    elif os.path.isfile(f"{filename}.java"):
        subprocess.run(["javac", f"{filename}.java"])
        command = f"java {filename}"
    elif os.path.isfile(f"{filename}.c"):
        subprocess.run(["gcc", "-o", f"{filename}", f"{filename}.c"])
        command = f"./{filename}"
    elif os.path.isfile(f"{filename}.cpp"):
        subprocess.run(["g++", "-o", f"{filename}", f"{filename}.cpp"])
        command = f"./{filename}"
    else:
        print(f"No valid file found for {filename}.")
        return

    # Dictionary to store execution times
    times = {}

    # Run the chosen command on each .in file and compare output to .ans file
    for in_file in input_files:
        ans_file = in_file.replace('.in', '.out')
        # Run the command and time it
        start_time = timeit.default_timer()

        try:
            output = subprocess.check_output(f"{command} < {in_file}", shell=True, timeout=3).decode()
        except subprocess.TimeoutExpired:
            print(f"Time limit exceeded for test case: {in_file}.")
            return
        except Exception as e:
            print(f"Error occurred while running test case {in_file}: {str(e)}")
            return

        elapsed = timeit.default_timer() - start_time
        times[in_file] = elapsed

        # Open the answer file and compare
        with open(ans_file, 'r') as f:
            ans = f.read()

        if ''.join(output).replace('\n','') == ''.join(ans).replace('\n',''):
            pass
        else:
            print("Fail, you have",output,'but expected',ans)
            return

    # Calculate the sum of the 6 highest times
    largest_6_times = heapq.nlargest(6, times.values())
    total_time = sum(largest_6_times)

    # Check if total time exceeds 3 seconds
    if total_time > 3.0:
        print("0")
        print("The following tests contributed most to the execution time:")
        for file, time in times.items():
            if time in largest_6_times:
                print(f"{file}: {time}s")
    else:
        print("1")

if __name__ == "__main__":
    main()
