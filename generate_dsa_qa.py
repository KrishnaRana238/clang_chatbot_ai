import json
import random

topics = [
    "arrays", "strings", "linked lists", "binary trees", "graphs", "sorting", "searching", "dynamic programming", "greedy", "stacks", "queues", "hashing", "recursion", "backtracking", "heaps", "tries", "bit manipulation", "math", "geometry", "number theory"
]

languages = ["Python", "C++", "Java"]

code_templates = {
    "Python": {
        "arrays": """```python\ndef find_max(arr):\n    return max(arr)\n```\nFinds the maximum element in an array.""",
        "strings": """```python\ndef reverse_string(s):\n    return s[::-1]\n```\nReverses a string.""",
        "linked lists": """```python\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        next_node = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_node\n    return prev\n```\nReverses a singly linked list.""",
        "binary trees": """```python\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef treeHeight(root):\n    if not root:\n        return 0\n    return 1 + max(treeHeight(root.left), treeHeight(root.right))\n```\nComputes the height of a binary tree.""",
        "sorting": """```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n```\nSorts an array using bubble sort.""",
        "searching": """```python\ndef binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n```\nPerforms binary search on a sorted array."""
    },
    "C++": {
        "arrays": """```cpp\n#include <iostream>\nusing namespace std;\nint findMax(int arr[], int n) {\n    int maxVal = arr[0];\n    for(int i=1;i<n;i++)\n        if(arr[i]>maxVal) maxVal=arr[i];\n    return maxVal;\n}\n```\nFinds the maximum element in an array.""",
        "strings": """```cpp\n#include <iostream>\n#include <algorithm>\nusing namespace std;\nstring reverseString(string s) {\n    reverse(s.begin(), s.end());\n    return s;\n}\n```\nReverses a string.""",
        "linked lists": """```cpp\nstruct ListNode {\n    int val;\n    ListNode* next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\nListNode* reverseList(ListNode* head) {\n    ListNode* prev = nullptr;\n    while (head) {\n        ListNode* next = head->next;\n        head->next = prev;\n        prev = head;\n        head = next;\n    }\n    return prev;\n}\n```\nReverses a singly linked list.""",
        "binary trees": """```cpp\nstruct TreeNode {\n    int val;\n    TreeNode* left;\n    TreeNode* right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\nint treeHeight(TreeNode* root) {\n    if (!root) return 0;\n    return 1 + max(treeHeight(root->left), treeHeight(root->right));\n}\n```\nComputes the height of a binary tree.""",
        "sorting": """```cpp\nvoid bubbleSort(int arr[], int n) {\n    for(int i=0;i<n-1;i++)\n        for(int j=0;j<n-i-1;j++)\n            if(arr[j]>arr[j+1]) swap(arr[j],arr[j+1]);\n}\n```\nSorts an array using bubble sort.""",
        "searching": """```cpp\nint binarySearch(int arr[], int n, int target) {\n    int left=0,right=n-1;\n    while(left<=right){\n        int mid=left+(right-left)/2;\n        if(arr[mid]==target) return mid;\n        else if(arr[mid]<target) left=mid+1;\n        else right=mid-1;\n    }\n    return -1;\n}\n```\nPerforms binary search on a sorted array."""
    },
    "Java": {
        "arrays": """```java\npublic int findMax(int[] arr) {\n    int maxVal = arr[0];\n    for(int i=1;i<arr.length;i++)\n        if(arr[i]>maxVal) maxVal=arr[i];\n    return maxVal;\n}\n```\nFinds the maximum element in an array.""",
        "strings": """```java\npublic String reverseString(String s) {\n    return new StringBuilder(s).reverse().toString();\n}\n```\nReverses a string.""",
        "linked lists": """```java\nclass ListNode {\n    int val;\n    ListNode next;\n    ListNode(int x) { val = x; }\n}\npublic ListNode reverseList(ListNode head) {\n    ListNode prev = null;\n    while (head != null) {\n        ListNode next = head.next;\n        head.next = prev;\n        prev = head;\n        head = next;\n    }\n    return prev;\n}\n```\nReverses a singly linked list.""",
        "binary trees": """```java\nclass TreeNode {\n    int val;\n    TreeNode left, right;\n    TreeNode(int x) { val = x; }\n}\npublic int treeHeight(TreeNode root) {\n    if (root == null) return 0;\n    return 1 + Math.max(treeHeight(root.left), treeHeight(root.right));\n}\n```\nComputes the height of a binary tree.""",
        "sorting": """```java\npublic void bubbleSort(int[] arr) {\n    int n = arr.length;\n    for(int i=0;i<n-1;i++)\n        for(int j=0;j<n-i-1;j++)\n            if(arr[j]>arr[j+1]) {\n                int temp=arr[j];arr[j]=arr[j+1];arr[j+1]=temp;\n            }\n}\n```\nSorts an array using bubble sort.""",
        "searching": """```java\npublic int binarySearch(int[] arr, int target) {\n    int left=0,right=arr.length-1;\n    while(left<=right){\n        int mid=left+(right-left)/2;\n        if(arr[mid]==target) return mid;\n        else if(arr[mid]<target) left=mid+1;\n        else right=mid-1;\n    }\n    return -1;\n}\n```\nPerforms binary search on a sorted array."""
    }
}

def generate_problem(idx):
    topic = random.choice(topics)
    lang = random.choice(languages)
    base_question = f"[{idx+1}] Solve a {topic} problem. Code in {lang}."
    # Use a template if available, else generic
    answer = code_templates.get(lang, {}).get(topic, f"// Code for {topic} in {lang} not available.")
    return {
        "question": base_question,
        "answer": answer
    }

problems = [generate_problem(i) for i in range(1000)]

with open("dsa_training_data_template.json", "w") as f:
    json.dump(problems, f, indent=2)
