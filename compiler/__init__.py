from .AVAIL import avail
from .parser import global_context, parser
from .Quadruple import Quadruple


def parse(file: str, debug: bool = False):
    input_data = ""
    with open(file, "r") as input_file:
        input_data = "".join(input_file.readlines())
    parse_status = parser.parse(input_data, tracking=True, debug=debug)
    return parse_status == "COMPILA"


def export(file: str):
    with open(file, "w+") as export_file:
        export_file.write("%%\n")
        for value, direction in avail.const_to_dir.items():
            export_file.write(f"{direction},{value}\n")
        export_file.write("%%\n")
        for func in global_context.function_table.table.values():
            export_file.write(f"{func.name},{func.return_type}," +
                              f"{func.quad_number}," +
                              f"{[(k, v) for k, v in func.vars.items()]}," +
                              f"{[(k, v) for k, v in func.temps.items()]}\n")
        export_file.write("%%\n")
        for quad in range(len(global_context.quadruples)):
            # print(quad, global_context.quadruples[quad])
            quadruple = global_context.quadruples[quad]
            try:
                quad_name = Quadruple.OperationType[quadruple.operation].value
                # print("NAME", quad_name)
            except KeyError:
                quad_name = quadruple.operation
            line = f"{quad_name},{quadruple.first_direction},{quadruple.second_direction},{quadruple.result}\n"
            # print(line)
            export_file.write(line)