import os


def generator_project(project_name):
    if os.path.exists(project_name):
        print(f'project "{project_name}" already exists')
        return
    os.mkdir("./" + project_name)
    with open(f"./{project_name}/main.md", 'w') as f:
        pass
    with open(f"./{project_name}/main.json", 'w') as f:
        pass


if __name__ == '__main__':
    generator_project("test")
