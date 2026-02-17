"""
0-1背包问题的Python实现

0-1背包问题：给定一组物品，每个物品有重量和价值，在背包容量限制下，
选择物品使得总价值最大，且每个物品只能选择0次或1次。

算法范式：动态规划
时间复杂度：O(n * capacity)
空间复杂度：O(n * capacity) 或 O(capacity)（优化后）
"""

def knapsack_01_dp(weights, values, capacity):
    """
    0-1背包问题的动态规划解法（二维数组）
    
    参数：
        weights: list[int] - 物品重量列表
        values: list[int] - 物品价值列表
        capacity: int - 背包容量
        
    返回：
        tuple: (最大价值, 选择的物品索引列表)
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []
    
    # 检查输入有效性
    if len(values) != n:
        raise ValueError("weights和values长度必须相同")
    if any(w <= 0 for w in weights):
        raise ValueError("物品重量必须为正数")
    if any(v < 0 for v in values):
        raise ValueError("物品价值不能为负数")
    
    # 创建DP表：dp[i][w]表示前i个物品在容量w下的最大价值
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # 填充DP表
    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for w in range(1, capacity + 1):
            if weight > w:
                # 当前物品太重，无法放入
                dp[i][w] = dp[i - 1][w]
            else:
                # 选择放入或不放入当前物品中的最大值
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
    
    # 回溯找出选择的物品
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            # 第i个物品被选中
            selected_items.append(i - 1)
            w -= weights[i - 1]
    
    selected_items.reverse()  # 按原始顺序排序
    max_value = dp[n][capacity]
    
    return max_value, selected_items


def knapsack_01_dp_optimized(weights, values, capacity):
    """
    0-1背包问题的动态规划解法（空间优化版）
    
    使用一维数组优化空间复杂度：O(capacity)
    注意：内层循环需要逆序遍历，确保每个物品只被考虑一次
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []
    
    # 检查输入有效性
    if len(values) != n:
        raise ValueError("weights和values长度必须相同")
    
    # 创建一维DP数组：dp[w]表示容量w下的最大价值
    dp = [0] * (capacity + 1)
    # 用于记录选择的物品（可选，会稍微增加复杂度）
    item_selection = [[] for _ in range(capacity + 1)]
    
    for i in range(n):
        weight = weights[i]
        value = values[i]
        # 逆序遍历，确保每个物品只使用一次
        for w in range(capacity, weight - 1, -1):
            if dp[w - weight] + value > dp[w]:
                dp[w] = dp[w - weight] + value
                # 记录选择的物品（需要复制列表）
                item_selection[w] = item_selection[w - weight] + [i]
    
    max_value = dp[capacity]
    selected_items = item_selection[capacity]
    
    return max_value, selected_items


def knapsack_01_bruteforce(weights, values, capacity):
    """
    0-1背包问题的暴力解法（回溯法）
    
    适用于物品数量较少的情况（n <= 20）
    算法范式：回溯法/深度优先搜索
    时间复杂度：O(2^n)
    """
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []
    
    best_value = 0
    best_selection = []
    
    def backtrack(idx, current_weight, current_value, selected):
        nonlocal best_value, best_selection
        
        if idx == n:
            if current_value > best_value:
                best_value = current_value
                best_selection = selected.copy()
            return
        
        # 不选当前物品
        backtrack(idx + 1, current_weight, current_value, selected)
        
        # 选当前物品（如果容量允许）
        if current_weight + weights[idx] <= capacity:
            selected.append(idx)
            backtrack(idx + 1, 
                     current_weight + weights[idx], 
                     current_value + values[idx], 
                     selected)
            selected.pop()  # 回溯
    
    backtrack(0, 0, 0, [])
    return best_value, best_selection


def knapsack_01_branch_bound(weights, values, capacity):
    """
    0-1背包问题的分支限界法
    
    算法范式：分支限界法
    使用优先队列（最大堆）按价值密度排序
    时间复杂度：最坏情况O(2^n)，但通常比回溯法快
    """
    import heapq
    
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []
    
    # 计算价值密度并排序
    items = [(values[i] / weights[i] if weights[i] > 0 else 0, 
              weights[i], values[i], i) 
             for i in range(n)]
    items.sort(reverse=True)  # 按价值密度降序排列
    
    # 计算上界函数（贪心解）
    def calculate_upper_bound(idx, remaining_capacity, current_value):
        bound = current_value
        temp_capacity = remaining_capacity
        i = idx
        
        while i < n and temp_capacity >= items[i][1]:
            density, weight, value, _ = items[i]
            bound += value
            temp_capacity -= weight
            i += 1
        
        # 如果还有剩余容量，加入部分物品（分数背包）
        if i < n and temp_capacity > 0:
            density, weight, value, _ = items[i]
            bound += density * temp_capacity
        
        return bound
    
    # 优先队列元素：(上界, 当前价值, 剩余容量, 索引, 选择状态)
    # 使用负的上界实现最大堆
    best_value = 0
    best_selection = []
    
    # 初始节点
    initial_bound = calculate_upper_bound(0, capacity, 0)
    heap = [(-initial_bound, 0, capacity, 0, [])]  # 负值用于最大堆
    
    while heap:
        neg_bound, current_value, remaining_capacity, idx, selected = heapq.heappop(heap)
        bound = -neg_bound
        
        # 如果当前上界小于已知最优解，剪枝
        if bound <= best_value:
            continue
        
        if idx == n:
            if current_value > best_value:
                best_value = current_value
                best_selection = selected.copy()
            continue
        
        density, weight, value, original_idx = items[idx]
        
        # 不选当前物品
        new_bound = calculate_upper_bound(idx + 1, remaining_capacity, current_value)
        if new_bound > best_value:
            heapq.heappush(heap, (-new_bound, current_value, remaining_capacity, idx + 1, selected))
        
        # 选当前物品（如果容量允许）
        if remaining_capacity >= weight:
            new_value = current_value + value
            new_capacity = remaining_capacity - weight
            new_selected = selected + [original_idx]
            
            if new_value > best_value:
                best_value = new_value
                best_selection = new_selected
            
            new_bound = calculate_upper_bound(idx + 1, new_capacity, new_value)
            if new_bound > best_value:
                heapq.heappush(heap, (-new_bound, new_value, new_capacity, idx + 1, new_selected))
    
    # 按原始索引排序
    best_selection.sort()
    return best_value, best_selection


def test_knapsack():
    """测试函数，验证各种算法的正确性"""
    print("=== 0-1背包算法测试 ===\n")
    
    # 测试用例1：标准示例
    weights1 = [2, 3, 4, 5]
    values1 = [3, 4, 5, 6]
    capacity1 = 8
    
    print(f"测试用例1:")
    print(f"物品重量: {weights1}")
    print(f"物品价值: {values1}")
    print(f"背包容量: {capacity1}")
    
    # 测试各种算法
    algorithms = [
        ("动态规划（二维）", knapsack_01_dp),
        ("动态规划（空间优化）", knapsack_01_dp_optimized),
        ("回溯法（暴力）", knapsack_01_bruteforce),
        ("分支限界法", knapsack_01_branch_bound),
    ]
    
    results = {}
    for name, func in algorithms:
        try:
            max_value, selected = func(weights1, values1, capacity1)
            results[name] = (max_value, selected)
            print(f"\n{name}:")
            print(f"  最大价值: {max_value}")
            print(f"  选择的物品索引: {selected}")
            print(f"  总重量: {sum(weights1[i] for i in selected)}")
        except Exception as e:
            print(f"\n{name} 错误: {e}")
    
    # 验证所有算法结果一致
    if len(results) > 1:
        first_result = next(iter(results.values()))
        all_same = all(result[0] == first_result[0] for result in results.values())
        if all_same:
            print(f"\n✓ 所有算法结果一致: 最大价值 = {first_result[0]}")
        else:
            print("\n✗ 算法结果不一致!")
            for name, (value, _) in results.items():
                print(f"  {name}: {value}")
    
    # 测试用例2：边界情况
    print("\n\n测试用例2: 边界情况")
    weights2 = []
    values2 = []
    capacity2 = 10
    max_value, selected = knapsack_01_dp(weights2, values2, capacity2)
    print(f"空物品列表: 最大价值={max_value}, 选择的物品={selected}")
    
    # 测试用例3：大容量
    print("\n\n测试用例3: 所有物品都能放入")
    weights3 = [1, 2, 3]
    values3 = [10, 20, 30]
    capacity3 = 10
    max_value, selected = knapsack_01_dp(weights3, values3, capacity3)
    print(f"所有物品都能放入: 最大价值={max_value}, 选择的物品={selected}")
    
    # 测试用例4：性能测试
    print("\n\n测试用例4: 性能比较（10个物品）")
    import random
    random.seed(42)
    n = 10
    weights4 = [random.randint(1, 20) for _ in range(n)]
    values4 = [random.randint(1, 50) for _ in range(n)]
    capacity4 = sum(weights4) // 2
    
    print(f"物品数量: {n}")
    print(f"容量: {capacity4}")
    
    import time
    for name, func in algorithms[:2]:  # 只测试DP算法，回溯和分支限界可能较慢
        start = time.time()
        max_value, selected = func(weights4, values4, capacity4)
        elapsed = time.time() - start
        print(f"{name}: 最大价值={max_value}, 时间={elapsed:.4f}秒")


def main():
    """主函数，提供命令行接口"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_knapsack()
        return
    
    # 交互式示例
    print("0-1背包问题求解器")
    print("=" * 40)
    
    # 示例数据
    weights = [2, 3, 4, 5, 7]
    values = [3, 4, 5, 6, 8]
    capacity = 10
    
    print(f"示例数据:")
    print(f"物品重量: {weights}")
    print(f"物品价值: {values}")
    print(f"背包容量: {capacity}")
    
    print("\n选择算法:")
    print("1. 动态规划（二维数组）")
    print("2. 动态规划（空间优化）")
    print("3. 回溯法（暴力搜索，适用于n≤20）")
    print("4. 分支限界法（优先队列）")
    
    try:
        choice = input("\n请输入算法编号 (1-4, 默认1): ").strip()
        if choice == "":
            choice = "1"
        
        algorithms = {
            "1": knapsack_01_dp,
            "2": knapsack_01_dp_optimized,
            "3": knapsack_01_bruteforce,
            "4": knapsack_01_branch_bound,
        }
        
        if choice not in algorithms:
            print("无效选择，使用默认算法（动态规划）")
            choice = "1"
        
        algorithm = algorithms[choice]
        max_value, selected_items = algorithm(weights, values, capacity)
        
        print(f"\n结果:")
        print(f"最大价值: {max_value}")
        print(f"选择的物品索引: {selected_items}")
        print(f"具体物品:")
        total_weight = 0
        total_value = 0
        for idx in selected_items:
            weight = weights[idx]
            value = values[idx]
            total_weight += weight
            total_value += value
            print(f"  物品{idx}: 重量={weight}, 价值={value}")
        
        print(f"\n统计:")
        print(f"  总重量: {total_weight}/{capacity}")
        print(f"  总价值: {total_value}")
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    # 直接运行时会执行测试
    test_knapsack()