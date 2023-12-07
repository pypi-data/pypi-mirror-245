import requests
import json
import traceback

url = "http://10.3.2.121:8302/solver/mixInteger"


def mix_integer_solver(problem_file, problem, solution_save=None):
    """
    混合正数求解功能，远程调用接口
    :param problem_file: str, 问题文件地址
    :param problem: str, 问题类型选择，一般为WPMS,FCMCNF,GISP
    :param solution_save: 默认为None，打印求解结果；如果是str类型, 表示保存路径
    """
    data = {"file_name": problem_file}
    try:
        with open(problem_file, 'r') as f:
            lines = list(f.readlines())
    except Exception as e:
        raise traceback.format_exc()
    data['file'] = lines
    data["problem"] = problem
    try:
        response = requests.post(url, data=json.dumps(data))
    except Exception as e:
        raise traceback.format_exc()
    res = json.loads(response.text)
    code = res["code"]
    if code == 200:
        solution_info = res["res"]
        solver_time = solution_info["solveTime"]
        best_sol = solution_info["best_sol"]
        status = solution_info["status"]
        if solution_save:
            with open(solution_save, "w") as f:
                f.write(best_sol)
            print("Time Consuming(s):", solver_time)
            print("Solotion Status:", status)
            print("Saved File:", solution_save)
        else:
            print("Time Consuming(s):", solver_time)
            print("Solotion Status:", status)
            print("Best Solution:", best_sol)
    else:
        print(res["message"])


if __name__ == "__main__":
    file_name = "D:\\WorkSpace\\Development\\Solver\\node_selector\\data\\data\\WPMS\\test\\n=60_m=468_id_20.85.lp"
    mix_integer_solver(file_name, problem="FCMCNF", solution_save="./solve_out.txt")



