md = """
As your writing and programming assistant, I can provide you with the following services：

1. Writing：
    - Help you write articles, reports, essays, stories, etc.. 
    - Provide writing advice and tips. 
    - Assist you in copywriting and content creation. 

2. Programming：
    - Help you solve programming problems, Provide programming ideas and suggestions. 
    - Assist you in writing code, Including but not limited to Python, Java, C++, etc.. 
    - Explain complex technical concepts to you, Make it easier for you to understand. 

3. Project support：
    - Assist you in planning project schedules and task assignments. 
    - Provide project management and collaboration advice. 
    - Provide support during project implementation, Ensure the smooth progress of the project. 

4. Learning guidance：
    - Help you consolidate your programming foundation, Improve programming skills. 
    - Provide learning resources and advice in computer science, data science, artificial intelligence, and other related fields. 
    - Answer the questions you encounter during the learning process, Help you better grasp knowledge. 

5. Industry dynamics and trend analysis：
    - Providing you with the latest industry news and technology trends. 
    - Analyze industry trends, Help you understand market development and competitive situation. 
    - Provide reference and advice for developing your technical strategy. 

Please feel free to tell me your needs, I will do my best to provide assistance. If you have any questions or topics that need answers, Please feel free to ask. 
"""

def validate_path():
    import os, sys
    dir_name = os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(os.path.dirname(__file__) +  '/..')
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)
validate_path() # validate path so you can run from base directory
from void_terminal.toolbox import markdown_convertion

html = markdown_convertion(md)
print(html)
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(html)