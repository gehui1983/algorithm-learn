"""
B+树实现
B+树是一种自平衡的树数据结构，常用于数据库和文件系统中。
特点：
1. 所有键值都存储在叶子节点中，内部节点只存储键
2. 叶子节点之间通过指针连接，便于范围查询
3. 保持树的高度平衡，所有叶子节点在同一层
"""

from typing import List, Optional, Tuple, Union, Any


class BPlusTreeNode:
    """B+树节点基类"""
    
    def __init__(self, is_leaf: bool = False):
        self.is_leaf = is_leaf
        self.keys: List[Any] = []
        self.parent: Optional['BPlusTreeNode'] = None
    
    def is_full(self, order: int) -> bool:
        """检查节点是否已满"""
        return len(self.keys) >= order
    
    def is_underflow(self, order: int) -> bool:
        """检查节点是否过少（需要合并）"""
        # 根节点特殊处理
        if self.parent is None:
            return len(self.keys) < 1  # 根节点至少有一个键（除非树为空）
        return len(self.keys) < (order // 2)
    
    def __repr__(self) -> str:
        return f"{'Leaf' if self.is_leaf else 'Internal'}Node(keys={self.keys})"


class BPlusTreeLeafNode(BPlusTreeNode):
    """B+树叶节点"""
    
    def __init__(self):
        super().__init__(is_leaf=True)
        self.values: List[Any] = []
        self.next_leaf: Optional['BPlusTreeLeafNode'] = None  # 指向下一个叶子节点
    
    def insert(self, key: Any, value: Any, order: int) -> Tuple[bool, Optional['BPlusTreeLeafNode']]:
        """
        向叶子节点插入键值对
        返回: (是否成功, 分裂产生的新节点)
        """
        # 找到插入位置
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        
        # 如果键已存在，更新值
        if idx < len(self.keys) and self.keys[idx] == key:
            self.values[idx] = value
            return True, None
        
        # 插入键值对
        self.keys.insert(idx, key)
        self.values.insert(idx, value)
        
        # 检查是否需要分裂
        if self.is_full(order):
            return True, self._split(order)
        
        return True, None
    
    def _split(self, order: int) -> 'BPlusTreeLeafNode':
        """分裂叶子节点"""
        mid = order // 2
        new_leaf = BPlusTreeLeafNode()
        
        # 将后半部分的键值对移动到新节点
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        
        # 更新链表指针
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf
        new_leaf.parent = self.parent
        
        return new_leaf
    
    def search(self, key: Any) -> Optional[Any]:
        """在叶子节点中搜索键"""
        try:
            idx = self.keys.index(key)
            return self.values[idx]
        except ValueError:
            return None
    
    def delete(self, key: Any, order: int) -> bool:
        """从叶子节点删除键值对"""
        try:
            idx = self.keys.index(key)
            self.keys.pop(idx)
            self.values.pop(idx)
            return True
        except ValueError:
            return False
    
    def range_query(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """范围查询"""
        result = []
        current = self
        
        while current is not None:
            for i, key in enumerate(current.keys):
                if start_key <= key <= end_key:
                    result.append((key, current.values[i]))
                elif key > end_key:
                    return result
            current = current.next_leaf
        
        return result


class BPlusTreeInternalNode(BPlusTreeNode):
    """B+树内部节点"""
    
    def __init__(self):
        super().__init__(is_leaf=False)
        self.children: List[BPlusTreeNode] = []
    
    def insert_child(self, key: Any, child: BPlusTreeNode, order: int) -> Tuple[bool, Optional[Tuple['BPlusTreeInternalNode', Any]]]:
        """
        向内部节点插入子节点
        返回: (是否成功, (分裂产生的新节点, 分裂键) 或 None)
        """
        # 找到插入位置
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        
        # 插入键和子节点
        self.keys.insert(idx, key)
        self.children.insert(idx + 1, child)
        child.parent = self
        
        # 检查是否需要分裂
        if self.is_full(order):
            new_node, split_key = self._split(order)
            return True, (new_node, split_key)
        
        return True, None
    
    def _split(self, order: int) -> Tuple['BPlusTreeInternalNode', Any]:
        """分裂内部节点，返回新节点和分裂键"""
        mid = order // 2
        new_internal = BPlusTreeInternalNode()
        
        # 分裂键
        split_key = self.keys[mid]
        new_internal.keys = self.keys[mid + 1:]
        self.keys = self.keys[:mid]
        
        # 分裂子节点
        new_internal.children = self.children[mid + 1:]
        self.children = self.children[:mid + 1]
        
        # 更新父节点引用
        for child in new_internal.children:
            child.parent = new_internal
        
        new_internal.parent = self.parent
        
        return new_internal, split_key
    
    def get_child_index(self, key: Any) -> int:
        """根据键找到子节点索引"""
        idx = 0
        while idx < len(self.keys) and key >= self.keys[idx]:
            idx += 1
        return idx


class BPlusTree:
    """B+树主类"""
    
    def __init__(self, order: int = 4):
        """
        初始化B+树
        
        Args:
            order: B+树的阶数，决定每个节点的最大键数
        """
        if order < 3:
            raise ValueError("Order must be at least 3")
        
        self.order = order
        self.root: Optional[BPlusTreeNode] = BPlusTreeLeafNode()
        self.height = 1
    
    def search(self, key: Any) -> Optional[Any]:
        """搜索键对应的值"""
        node = self._find_leaf(key)
        if node is None:
            return None
        return node.search(key)
    
    def _find_leaf(self, key: Any) -> Optional[BPlusTreeLeafNode]:
        """找到包含给定键的叶子节点"""
        current = self.root
        
        while current is not None and not current.is_leaf:
            if isinstance(current, BPlusTreeInternalNode):
                idx = current.get_child_index(key)
                current = current.children[idx]
            else:
                break
        
        return current if isinstance(current, BPlusTreeLeafNode) else None
    
    def insert(self, key: Any, value: Any) -> bool:
        """插入键值对"""
        # 找到叶子节点
        leaf = self._find_leaf(key)
        if leaf is None:
            return False
        
        # 在叶子节点插入
        success, new_node = leaf.insert(key, value, self.order)
        
        if new_node is not None:
            self._handle_split(leaf, new_node)
        
        return success
    
    def _handle_split(self, old_node: BPlusTreeNode, new_node: BPlusTreeNode) -> None:
        """处理节点分裂"""
        # 如果旧节点是根节点，创建新的根节点
        if old_node.parent is None:
            new_root = BPlusTreeInternalNode()
            new_root.keys = [new_node.keys[0]]
            new_root.children = [old_node, new_node]
            old_node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
            self.height += 1
            return
        
        # 否则，将新节点插入到父节点
        parent = old_node.parent
        split_key = new_node.keys[0]
        
        success, result = parent.insert_child(split_key, new_node, self.order)
        
        if result is not None:
            # 父节点也分裂了
            if isinstance(result, tuple):
                new_parent, parent_split_key = result
                self._handle_split(parent, new_parent)
            else:
                self._handle_split(parent, result)
    
    def delete(self, key: Any) -> bool:
        """删除键值对"""
        leaf = self._find_leaf(key)
        if leaf is None:
            return False
        
        # 从叶子节点删除
        success = leaf.delete(key, self.order)
        if not success:
            return False
        
        # 检查是否下溢，需要处理
        if leaf.is_underflow(self.order):
            self._handle_underflow(leaf)
        
        return True
    
    def _handle_underflow(self, node: BPlusTreeNode) -> None:
        """处理节点下溢"""
        # TODO: 实现节点合并和重新分配
        pass
    
    def range_query(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """范围查询"""
        start_leaf = self._find_leaf(start_key)
        if start_leaf is None:
            return []
        
        return start_leaf.range_query(start_key, end_key)
    
    def traverse(self) -> List[Any]:
        """遍历所有键（有序）"""
        result = []
        
        # 找到最左边的叶子节点
        current = self.root
        while current is not None and not current.is_leaf:
            if isinstance(current, BPlusTreeInternalNode):
                current = current.children[0]
            else:
                break
        
        # 遍历叶子节点链表
        leaf = current
        while leaf is not None:
            result.extend(leaf.keys)
            if isinstance(leaf, BPlusTreeLeafNode):
                leaf = leaf.next_leaf
            else:
                break
        
        return result
    
    def __contains__(self, key: Any) -> bool:
        """检查键是否存在"""
        return self.search(key) is not None
    
    def __repr__(self) -> str:
        return f"BPlusTree(order={self.order}, height={self.height}, size={len(self.traverse())})"


if __name__ == "__main__":
    # 简单的测试
    tree = BPlusTree(order=4)
    
    # 插入一些数据
    data = [(10, "A"), (20, "B"), (5, "C"), (15, "D"), (25, "E"), (30, "F"), (35, "G")]
    
    print("插入数据...")
    for key, value in data:
        tree.insert(key, value)
        print(f"插入 ({key}, {value})")
    
    print(f"\n树状态: {tree}")
    print(f"所有键: {tree.traverse()}")
    
    # 搜索测试
    print("\n搜索测试:")
    test_keys = [10, 15, 40]
    for key in test_keys:
        result = tree.search(key)
        print(f"搜索 {key}: {'找到' if result else '未找到'} -> {result}")
    
    # 范围查询测试
    print("\n范围查询 [12, 32]:")
    range_result = tree.range_query(12, 32)
    for key, value in range_result:
        print(f"  {key}: {value}")
    
    # 删除测试
    print("\n删除键 15...")
    tree.delete(15)
    print(f"删除后所有键: {tree.traverse()}")
    print(f"15 是否在树中: {15 in tree}")