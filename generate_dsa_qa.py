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
        "searching": """```python\ndef binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n```\nPerforms binary search on a sorted array.""",
        "greedy": """```python\ndef activity_selection(activities):\n    activities.sort(key=lambda x: x[1])\n    res = [activities[0]]\n    for i in range(1, len(activities)):\n        if activities[i][0] >= res[-1][1]:\n            res.append(activities[i])\n    return res\n```\nSelects maximum number of non-overlapping activities.""",
        "recursion": """```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)\n```\nCalculates factorial using recursion.""",
        "queues": """```python\nfrom collections import deque\nq = deque()\nq.append(1)\nq.append(2)\nprint(q.popleft())\n```\nImplements a queue using deque.""",
        "tries": """```python\nclass TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word):\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                node.children[char] = TrieNode()\n            node = node.children[char]\n        node.is_end = True\n```\nBasic Trie implementation.""",
        "stacks": """```python\nstack = []\nstack.append(1)\nstack.append(2)\nprint(stack.pop())\n```\nImplements a stack using list.""",
        "heaps": """```python\nimport heapq\nh = []\nheapq.heappush(h, 3)\nheapq.heappush(h, 1)\nheapq.heappush(h, 2)\nprint(heapq.heappop(h))\n```\nImplements a min-heap using heapq.""",
        "hashing": """```python\nhash_map = {}\nhash_map['a'] = 1\nprint(hash_map['a'])\n```\nImplements a hash map using dict.""",
        "backtracking": """```python\ndef solve(nums, path):\n    if not nums:\n        print(path)\n        return\n    for i in range(len(nums)):\n        solve(nums[:i]+nums[i+1:], path+[nums[i]])\n```\nGenerates all permutations using backtracking.""",
        "bit manipulation": """```python\ndef count_set_bits(n):\n    count = 0\n    while n:\n        count += n & 1\n        n >>= 1\n    return count\n```\nCounts set bits in an integer.""",
        "math": """```python\ndef is_armstrong(n):\n    digits = [int(d) for d in str(n)]\n    power = len(digits)\n    return n == sum([d**power for d in digits])\n```\nChecks if a number is an Armstrong number.""",
        "geometry": """```python\ndef area_of_circle(r):\n    import math\n    return math.pi * r * r\n```\nCalculates area of a circle.""",
        "number theory": """```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True\n```\nChecks if a number is prime."""
    },
    "C++": {
        "arrays": """```cpp\n#include <iostream>\nusing namespace std;\nint findMax(int arr[], int n) {\n    int maxVal = arr[0];\n    for(int i=1;i<n;i++)\n        if(arr[i]>maxVal) maxVal=arr[i];\n    return maxVal;\n}\n```\nFinds the maximum element in an array.""",
        "strings": """```cpp\n#include <iostream>\n#include <algorithm>\nusing namespace std;\nstring reverseString(string s) {\n    reverse(s.begin(), s.end());\n    return s;\n}\n```\nReverses a string.""",
        "linked lists": """```cpp\nstruct ListNode {\n    int val;\n    ListNode* next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};\nListNode* reverseList(ListNode* head) {\n    ListNode* prev = nullptr;\n    while (head) {\n        ListNode* next = head->next;\n        head->next = prev;\n        prev = head;\n        head = next;\n    }\n    return prev;\n}\n```\nReverses a singly linked list.""",
        "binary trees": """```cpp\nstruct TreeNode {\n    int val;\n    TreeNode* left;\n    TreeNode* right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\nint treeHeight(TreeNode* root) {\n    if (!root) return 0;\n    return 1 + max(treeHeight(root->left), treeHeight(root->right));\n}\n```\nComputes the height of a binary tree.""",
        "sorting": """```cpp\nvoid bubbleSort(int arr[], int n) {\n    for(int i=0;i<n-1;i++)\n        for(int j=0;j<n-i-1;j++)\n            if(arr[j]>arr[j+1]) swap(arr[j],arr[j+1]);\n}\n```\nSorts an array using bubble sort.""",
        "searching": """```cpp\nint binarySearch(int arr[], int n, int target) {\n    int left=0,right=n-1;\n    while(left<=right){\n        int mid=left+(right-left)/2;\n        if(arr[mid]==target) return mid;\n        else if(arr[mid]<target) left=mid+1;\n        else right=mid-1;\n    }\n    return -1;\n}\n```\nPerforms binary search on a sorted array.""",
        "greedy": """```cpp\n#include <vector>\n#include <algorithm>\nusing namespace std;\nvector<pair<int,int>> activitySelection(vector<pair<int,int>>& activities) {\n    sort(activities.begin(), activities.end(), [](auto &a, auto &b){ return a.second < b.second; });\n    vector<pair<int,int>> res;\n    res.push_back(activities[0]);\n    for (size_t i = 1; i < activities.size(); ++i) {\n        if (activities[i].first >= res.back().second)\n            res.push_back(activities[i]);\n    }\n    return res;\n}\n```\nSelects maximum number of non-overlapping activities.""",
        "recursion": """```cpp\nint factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n-1);\n}\n```\nCalculates factorial using recursion.""",
        "queues": """```cpp\n#include <queue>\n#include <iostream>\nusing namespace std;\nqueue<int> q;\nq.push(1);\nq.push(2);\ncout << q.front() << endl;\nq.pop();\n```\nImplements a queue using STL queue.""",
        "tries": """```cpp\n#include <unordered_map>\nclass TrieNode {\npublic:\n    unordered_map<char, TrieNode*> children;\n    bool is_end = false;\n};\nclass Trie {\npublic:\n    TrieNode* root = new TrieNode();\n    void insert(string word) {\n        TrieNode* node = root;\n        for (char c : word) {\n            if (!node->children[c]) node->children[c] = new TrieNode();\n            node = node->children[c];\n        }\n        node->is_end = true;\n    }\n};\n```\nBasic Trie implementation.""",
        "stacks": """```cpp\n#include <stack>\n#include <iostream>\nusing namespace std;\nstack<int> s;\ns.push(1);\ns.push(2);\ncout << s.top() << endl;\ns.pop();\n```\nImplements a stack using STL stack.""",
        "heaps": """```cpp\n#include <queue>\n#include <vector>\n#include <iostream>\nusing namespace std;\npriority_queue<int, vector<int>, greater<int>> h;\nh.push(3);\nh.push(1);\nh.push(2);\ncout << h.top() << endl;\nh.pop();\n```\nImplements a min-heap using STL priority_queue.""",
        "hashing": """```cpp\n#include <unordered_map>\n#include <iostream>\nusing namespace std;\nunordered_map<string, int> hash_map;\nhash_map["a"] = 1;\ncout << hash_map["a"] << endl;\n```\nImplements a hash map using unordered_map.""",
        "backtracking": """```cpp\n#include <vector>\n#include <iostream>\nusing namespace std;\nvoid solve(vector<int>& nums, vector<int>& path) {\n    if (nums.empty()) {\n        for (int x : path) cout << x << " ";\n        cout << endl;\n        return;\n    }\n    for (size_t i = 0; i < nums.size(); ++i) {\n        vector<int> nums2 = nums;\n        nums2.erase(nums2.begin() + i);\n        vector<int> path2 = path;\n        path2.push_back(nums[i]);\n        solve(nums2, path2);\n    }\n}\n```\nGenerates all permutations using backtracking.""",
        "bit manipulation": """```cpp\nint countSetBits(int n) {\n    int count = 0;\n    while (n) {\n        count += n & 1;\n        n >>= 1;\n    }\n    return count;\n}\n```\nCounts set bits in an integer.""",
        "math": """```cpp\n#include <cmath>\nbool isArmstrong(int n) {\n    int temp = n, digitCount = 0, sum = 0;\n    digitCount = (int)(log10(n)) + 1;\n    while (temp != 0) {\n        int digit = temp % 10;\n        sum += pow(digit, digitCount);\n        temp /= 10;\n    }\n    return n == sum;\n}\n```\nChecks if a number is an Armstrong number.""",
        "geometry": """```cpp\n#include <cmath>\ndouble areaOfCircle(double r) {\n    return M_PI * r * r;\n}\n```\nCalculates area of a circle.""",
        "number theory": """```cpp\nbool isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i * i <= n; ++i)\n        if (n % i == 0) return false;\n    return true;\n}\n```\nChecks if a number is prime."""
    },
    "Java": {
        "arrays": """```java\npublic int findMax(int[] arr) {\n    int maxVal = arr[0];\n    for(int i=1;i<arr.length;i++)\n        if(arr[i]>maxVal) maxVal=arr[i];\n    return maxVal;\n}\n```\nFinds the maximum element in an array.""",
        "strings": """```java\npublic String reverseString(String s) {\n    return new StringBuilder(s).reverse().toString();\n}\n```\nReverses a string.""",
        "linked lists": """```java\nclass ListNode {\n    int val;\n    ListNode next;\n    ListNode(int x) { val = x; }\n}\npublic ListNode reverseList(ListNode head) {\n    ListNode prev = null;\n    while (head != null) {\n        ListNode next = head.next;\n        head.next = prev;\n        prev = head;\n        head = next;\n    }\n    return prev;\n}\n```\nReverses a singly linked list.""",
        "binary trees": """```java\nclass TreeNode {\n    int val;\n    TreeNode left, right;\n    TreeNode(int x) { val = x; }\n}\npublic int treeHeight(TreeNode root) {\n    if (root == null) return 0;\n    return 1 + Math.max(treeHeight(root.left), treeHeight(root.right));\n}\n```\nComputes the height of a binary tree.""",
        "sorting": """```java\npublic void bubbleSort(int[] arr) {\n    int n = arr.length;\n    for(int i=0;i<n-1;i++)\n        for(int j=0;j<n-i-1;j++)\n            if(arr[j]>arr[j+1]) {\n                int temp=arr[j];arr[j]=arr[j+1];arr[j+1]=temp;\n            }\n}\n```\nSorts an array using bubble sort.""",
        "searching": """```java\npublic int binarySearch(int[] arr, int target) {\n    int left=0,right=arr.length-1;\n    while(left<=right){\n        int mid=left+(right-left)/2;\n        if(arr[mid]==target) return mid;\n        else if(arr[mid]<target) left=mid+1;\n        else right=mid-1;\n    }\n    return -1;\n}\n```\nPerforms binary search on a sorted array.""",
        "greedy": """```java\nimport java.util.*;\npublic List<int[]> activitySelection(List<int[]> activities) {\n    activities.sort(Comparator.comparingInt(a -> a[1]));\n    List<int[]> res = new ArrayList<>();\n    res.add(activities.get(0));\n    for (int i = 1; i < activities.size(); i++) {\n        if (activities.get(i)[0] >= res.get(res.size()-1)[1])\n            res.add(activities.get(i));\n    }\n    return res;\n}\n```\nSelects maximum number of non-overlapping activities.""",
        "recursion": """```java\npublic int factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n-1);\n}\n```\nCalculates factorial using recursion.""",
        "queues": """```java\nimport java.util.*;\nQueue<Integer> q = new LinkedList<>();\nq.add(1);\nq.add(2);\nSystem.out.println(q.poll());\n```\nImplements a queue using LinkedList.""",
        "tries": """```java\nclass TrieNode {\n    Map<Character, TrieNode> children = new HashMap<>();\n    boolean isEnd = false;\n}\nclass Trie {\n    TrieNode root = new TrieNode();\n    void insert(String word) {\n        TrieNode node = root;\n        for (char c : word.toCharArray()) {\n            node.children.putIfAbsent(c, new TrieNode());\n            node = node.children.get(c);\n        }\n        node.isEnd = true;\n    }\n}\n```\nBasic Trie implementation.""",
        "stacks": """```java\nimport java.util.*;\nStack<Integer> stack = new Stack<>();\nstack.push(1);\nstack.push(2);\nSystem.out.println(stack.pop());\n```\nImplements a stack using Stack class.""",
        "heaps": """```java\nimport java.util.*;\nPriorityQueue<Integer> h = new PriorityQueue<>();\nh.add(3);\nh.add(1);\nh.add(2);\nSystem.out.println(h.poll());\n```\nImplements a min-heap using PriorityQueue.""",
        "hashing": """```java\nimport java.util.*;\nMap<String, Integer> hashMap = new HashMap<>();\nhashMap.put("a", 1);\nSystem.out.println(hashMap.get("a"));\n```\nImplements a hash map using HashMap.""",
        "backtracking": """```java\npublic void solve(List<Integer> nums, List<Integer> path) {\n    if (nums.isEmpty()) {\n        System.out.println(path);\n        return;\n    }\n    for (int i = 0; i < nums.size(); i++) {\n        List<Integer> nums2 = new ArrayList<>(nums);\n        nums2.remove(i);\n        List<Integer> path2 = new ArrayList<>(path);\n        path2.add(nums.get(i));\n        solve(nums2, path2);\n    }\n}\n```\nGenerates all permutations using backtracking.""",
        "bit manipulation": """```java\npublic int countSetBits(int n) {\n    int count = 0;\n    while (n != 0) {\n        count += n & 1;\n        n >>= 1;\n    }\n    return count;\n}\n```\nCounts set bits in an integer.""",
        "math": """```java\npublic boolean isArmstrong(int n) {\n    int temp = n, digitCount = 0, sum = 0;\n    digitCount = (int)(Math.log10(n)) + 1;\n    while (temp != 0) {\n        int digit = temp % 10;\n        sum += Math.pow(digit, digitCount);\n        temp /= 10;\n    }\n    return n == sum;\n}\n```\nChecks if a number is an Armstrong number.""",
        "geometry": """```java\npublic double areaOfCircle(double r) {\n    return Math.PI * r * r;\n}\n```\nCalculates area of a circle.""",
        "number theory": """```java\npublic boolean isPrime(int n) {\n    if (n < 2) return false;\n    for (int i = 2; i * i <= n; i++)\n        if (n % i == 0) return false;\n    return true;\n}\n```\nChecks if a number is prime."""
    },
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
