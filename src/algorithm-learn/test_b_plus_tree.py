#!/usr/bin/env python3
"""
B+树测试文件
测试B+树的各种操作和边界情况
"""

import sys
import random
from typing import List, Tuple
from b_plus_tree import BPlusTree


def test_basic_operations() -> None:
    """测试基本操作：插入、查找、删除"""
    print("=== 测试基本操作 ===")
    tree = BPlusTree(order=4)
    
    # 测试数据
    test_data = [
        (10, "A"), (20, "B"), (5, "C"), (15, "D"),
        (25, "E"), (30, "F"), (35, "G"), (3, "H"),
        (7, "I"), (12, "J"), (18, "K"), (22, "L")
    ]
    
    # 插入测试
    print("1. 插入测试...")
    for key, value in test_data:
        assert tree.insert(key, value), f"插入失败: ({key}, {value})"
    
    print(f"  树状态: {tree}")
    print(f"  所有键: {sorted([k for k, _ in test_data])}")
    print(f"  树中键: {tree.traverse()}")
    
    # 验证所有键都存在且有序
    assert tree.traverse() == sorted([k for k, _ in test_data]), "键顺序错误"
    
    # 查找测试
    print("\n2. 查找测试...")
    for key, expected_value in test_data:
        actual_value = tree.search(key)
        assert actual_value == expected_value, f"键 {key} 查找失败: 期望 {expected_value}, 实际 {actual_value}"
        print(f"  键 {key}: 找到值 {actual_value}")
    
    # 测试不存在的键
    non_existent_keys = [-1, 0, 100, 99]
    for key in non_existent_keys:
        assert tree.search(key) is None, f"不存在的键 {key} 不应找到"
    
    # 删除测试
    print("\n3. 删除测试...")
    keys_to_delete = [15, 5, 30, 10]
    for key in keys_to_delete:
        print(f"  删除键 {key}...")
        assert tree.delete(key), f"删除键 {key} 失败"
        assert tree.search(key) is None, f"删除后键 {key} 不应找到"
    
    # 验证剩余键
    remaining_keys = [k for k, _ in test_data if k not in keys_to_delete]
    print(f"  剩余键: {sorted(remaining_keys)}")
    print(f"  树中键: {tree.traverse()}")
    assert tree.traverse() == sorted(remaining_keys), "删除后键顺序错误"
    
    print("✅ 基本操作测试通过！")


def test_range_queries() -> None:
    """测试范围查询"""
    print("\n=== 测试范围查询 ===")
    tree = BPlusTree(order=4)
    
    # 插入有序数据
    data = [(i, f"value_{i}") for i in range(1, 21)]
    random.shuffle(data)  # 随机顺序插入
    
    for key, value in data:
        tree.insert(key, value)
    
    print(f"树状态: {tree}")
    
    # 测试各种范围查询
    test_ranges = [
        (5, 10, list(range(5, 11))),      # 正常范围
        (1, 20, list(range(1, 21))),      # 整个范围
        (15, 15, [15]),                   # 单点范围
        (0, 5, list(range(1, 6))),        # 部分超出下限
        (18, 25, list(range(18, 21))),    # 部分超出上限
        (25, 30, []),                     # 完全超出范围
        (-5, -1, []),                     # 完全在范围外（负值）
    ]
    
    for start, end, expected_keys in test_ranges:
        result = tree.range_query(start, end)
        actual_keys = [key for key, _ in result]
        assert actual_keys == expected_keys, \
            f"范围查询 [{start}, {end}] 失败: 期望 {expected_keys}, 实际 {actual_keys}"
        
        # 验证值正确性
        for key, value in result:
            assert value == f"value_{key}", f"键 {key} 的值错误: {value}"
        
        print(f"  范围 [{start}, {end}]: 找到 {len(result)} 个结果")
    
    print("✅ 范围查询测试通过！")


def test_edge_cases() -> None:
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 测试空树
    print("1. 测试空树...")
    empty_tree = BPlusTree(order=3)
    assert empty_tree.traverse() == [], "空树应返回空列表"
    assert empty_tree.search(1) is None, "空树搜索应返回None"
    assert empty_tree.range_query(1, 10) == [], "空树范围查询应返回空列表"
    assert not empty_tree.delete(1), "从空树删除应返回False"
    
    # 测试重复插入
    print("2. 测试重复插入...")
    tree = BPlusTree(order=4)
    tree.insert(10, "first")
    tree.insert(10, "second")  # 应更新值
    assert tree.search(10) == "second", "重复插入应更新值"
    
    # 测试单个元素
    print("3. 测试单个元素...")
    single_tree = BPlusTree(order=3)
    single_tree.insert(42, "answer")
    assert single_tree.traverse() == [42], "单个元素树遍历错误"
    assert single_tree.search(42) == "answer", "单个元素搜索错误"
    assert single_tree.range_query(40, 45) == [(42, "answer")], "单个元素范围查询错误"
    assert single_tree.delete(42), "删除单个元素失败"
    assert single_tree.traverse() == [], "删除后树应为空"
    
    # 测试最小阶数
    print("4. 测试最小阶数...")
    try:
        BPlusTree(order=2)
        assert False, "阶数小于3应抛出异常"
    except ValueError:
        print("  ✅ 最小阶数检查通过")
    
    print("✅ 边界情况测试通过！")


def test_node_splitting() -> None:
    """测试节点分裂"""
    print("\n=== 测试节点分裂 ===")
    
    # 测试阶数为3的树（更容易触发分裂）
    tree = BPlusTree(order=3)
    
    # 插入数据直到触发分裂
    print("插入数据触发分裂...")
    data = [(i, f"val_{i}") for i in range(1, 10)]
    
    for key, value in data:
        tree.insert(key, value)
        print(f"  插入 {key} 后树高: {tree.height}")
    
    print(f"最终树状态: {tree}")
    
    # 验证所有数据都存在
    for key, expected_value in data:
        actual_value = tree.search(key)
        assert actual_value == expected_value, f"键 {key} 丢失: {actual_value}"
    
    # 验证键有序
    assert tree.traverse() == list(range(1, 10)), "分裂后键顺序错误"
    
    print("✅ 节点分裂测试通过！")


def test_random_operations() -> None:
    """测试随机操作"""
    print("\n=== 测试随机操作 ===")
    
    tree = BPlusTree(order=5)
    reference_dict = {}
    
    # 随机插入
    print("1. 随机插入测试...")
    for _ in range(100):
        key = random.randint(1, 100)
        value = f"val_{key}_{random.randint(1, 1000)}"
        tree.insert(key, value)
        reference_dict[key] = value
    
    print(f"  插入后树状态: {tree}")
    
    # 验证所有插入的键都存在
    for key, expected_value in reference_dict.items():
        actual_value = tree.search(key)
        assert actual_value == expected_value, f"键 {key} 值不匹配"
    
    # 随机删除
    print("\n2. 随机删除测试...")
    keys_to_delete = random.sample(list(reference_dict.keys()), min(30, len(reference_dict)))
    
    for key in keys_to_delete:
        if key in reference_dict:
            assert tree.delete(key), f"删除键 {key} 失败"
            del reference_dict[key]
            assert tree.search(key) is None, f"删除后键 {key} 不应存在"
    
    print(f"  删除后树状态: {tree}")
    
    # 验证剩余键
    for key, expected_value in reference_dict.items():
        actual_value = tree.search(key)
        assert actual_value == expected_value, f"删除后键 {key} 值不匹配"
    
    # 验证顺序
    expected_keys = sorted(reference_dict.keys())
    actual_keys = tree.traverse()
    assert actual_keys == expected_keys, f"键顺序错误: 期望 {expected_keys}, 实际 {actual_keys}"
    
    print("✅ 随机操作测试通过！")


def test_performance() -> None:
    """测试性能"""
    print("\n=== 测试性能 ===")
    
    import time
    
    tree = BPlusTree(order=100)  # 使用较大的阶数
    num_elements = 1000
    
    # 插入性能
    print(f"插入 {num_elements} 个元素...")
    start_time = time.time()
    
    for i in range(num_elements):
        tree.insert(i, f"value_{i}")
    
    insert_time = time.time() - start_time
    print(f"  插入时间: {insert_time:.3f} 秒")
    print(f"  平均每次插入: {insert_time/num_elements*1000:.3f} 毫秒")
    
    # 搜索性能
    print(f"\n搜索 {num_elements} 个元素...")
    start_time = time.time()
    
    for i in range(num_elements):
        value = tree.search(i)
        assert value == f"value_{i}", f"搜索失败: {i}"
    
    search_time = time.time() - start_time
    print(f"  搜索时间: {search_time:.3f} 秒")
    print(f"  平均每次搜索: {search_time/num_elements*1000:.3f} 毫秒")
    
    # 范围查询性能
    print(f"\n范围查询测试...")
    start_time = time.time()
    
    for _ in range(10):
        start = random.randint(0, num_elements - 100)
        end = start + random.randint(10, 100)
        results = tree.range_query(start, end)
        assert len(results) == (end - start + 1), f"范围查询结果数量错误"
    
    range_time = time.time() - start_time
    print(f"  范围查询时间: {range_time:.3f} 秒")
    
    print("✅ 性能测试完成！")


def main() -> None:
    """运行所有测试"""
    print("开始B+树测试...\n")
    
    try:
        test_basic_operations()
        test_range_queries()
        test_edge_cases()
        test_node_splitting()
        test_random_operations()
        test_performance()
        
        print("\n" + "="*50)
        print("🎉 所有测试通过！")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未预期的错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()