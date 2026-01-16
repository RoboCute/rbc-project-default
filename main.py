import robocute as rbc
from robocute import (
    RBCNode,
    GraphDefinition,
    NodeDefinition,
    NodeConnection,
    GraphExecutor,
    NodeGraph,
)


def main():
    print(f"========== ROBOCUTE v{rbc.__version__}==============")
    graph_def = GraphDefinition(
        nodes=[
            NodeDefinition(
                node_id="n1", node_type="input_number", inputs={"value": "1.0"}
            ),
            NodeDefinition(
                node_id="n2", node_type="input_number", inputs={"value": "2.0"}
            ),
            NodeDefinition(node_id="sum", node_type="math_add"),
        ],
        connections=[
            NodeConnection(
                from_node="n1", from_output="output", to_node="sum", to_input="a"
            ),
            NodeConnection(
                from_node="n2", from_output="output", to_node="sum", to_input="b"
            ),
        ],
    )
    graph = NodeGraph.from_definition(graph_def, "simple_calc_graph")

    is_valid, error = graph.validate()

    if is_valid:
        execution_order = graph.topological_sort()
        if execution_order is None:
            print("\n 图存在循环")
        else:
            print(f"\n执行顺序: {' → '.join(execution_order)}")
    else:
        print(f"\n✗ 图验证失败: {error}")
        return

    executor = GraphExecutor(graph)

    def progress_callback(node_id, status):
        emoji = (
            "⏳"
            if status.value == "running"
            else "✓"
            if status.value == "completed"
            else "✗"
        )
        print(f"  {emoji} 节点 '{node_id}': {status.value}")

    executor.add_callback(progress_callback)

    result = executor.execute()

    print("Result: ", result)


if __name__ == "__main__":
    main()
