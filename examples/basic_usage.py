from repository2prompt import Repository2Prompt

def main():
    github_converter = Repository2Prompt("https://github.com/user/repo", output_format="markdown")
    github_result = github_converter.process()
    print("GitHub Repository Result:")
    print(github_result)
    
    local_converter = Repository2Prompt("path/to/local/repo", output_format="json")
    local_result = local_converter.process()
    print("\nLocal Repository Result:")
    print(local_result)

if __name__ == "__main__":
    main()