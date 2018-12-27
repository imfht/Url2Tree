from urllib.parse import urlparse
from urllib.request import urlopen


def load_data(domain):
    req = urlopen('https://url.fht.im/url_search?domain=%s' % domain)
    response = req.read().decode('utf-8')
    url_list = set([i[0:-1].split('?')[0] for i in response.split('\n')])
    return list(url_list)


def get_data(domain):
    url_list = load_data(domain=domain)

    # First build a list of all url segments: final item is the title/url dict
    paths = []
    for item in url_list:
        split = item.split('/')
        paths.append(split[2:-1])
        paths[-1].append(split[-1])

    # Loop over these paths, building the format as we go along
    TreeNode = {"name": urlparse(item).netloc, "children": []}

    tree = TreeNode
    for path in paths:
        prev = tree  # 初始根节点
        for step in path[1:-1]:
            node = None
            for child_node in prev['children']:
                if child_node['name'] == step:
                    node = child_node
            if not node:
                node = {"name": step, "children": []}
                prev['children'].append(node)
            prev = node
        prev['children'].append({'name': path[-1], 'children': []})

    def fix_child(node):
        if not node[1]:
            return
        rtn = []

        for node in node[1]:
            rtn.append(fix_child(node))
        return rtn

    return tree


if __name__ == '__main__':
    print(load_data("qq.com"))
