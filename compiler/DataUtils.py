from typing import List, Tuple, Union, Optional

from .CuboSemantico import CuboSemantico
from .Function import FunctionTable, Function
from Stack import Stack
from .Quadruple import Quadruple
from .AVAIL import avail
from .Variable import Variable


class ParsingContext(object):
    # stack de las llamadas de funciones
    function: Stack
    # variable que almacena el tipo de dato definido (int : a, b, c) => int
    var_type: str

    quadruples: List[Quadruple]
    jumpStack: Stack

    types: Stack
    operations: Stack
    operands: Stack
    dimensions: Stack

    func_calls: Stack
    param_counter: Stack

    semantic_cube: CuboSemantico()
    function_table: FunctionTable()

    def __init__(self):
        self.function = Stack()
        self.var_type = ''
        self.quadruples = []
        self.jumpStack = Stack()
        self.operands = Stack()
        self.operations = Stack()
        self.types = Stack()
        self.semantic_cube = CuboSemantico()
        self.function_table = FunctionTable()
        self.param_counter = Stack()
        self.func_calls = Stack()
        self.dimensions = Stack()

    @property
    def quad_counter(self):
        # el indice inicia en 0
        return len(self.quadruples) - 1

    def add_function_parameter(self, var: Variable) -> bool:
        """
        Funcion que agrega un parametro a una funcion

        :param var: variable a agregar como parametro
        :return: regresa si se logro agregar el parametro
        """
        if self.function.top() == "global":
            var.direction = avail.get_next_global(var.type, False, var.name)
        else:
            var.direction = avail.get_next_local(var.type, False, var.name)

        if self.function_table.add_parameter(self.function.top(), var):
            return True
        return False

    def declare_function(self, f_name: str, f_type: Optional[str]) -> bool:
        """
        Funcion que declara una funcion
        :param f_name: nombre de la funcion
        :param f_type: tipo de retorno de la funcion
        :return: regresa si se logro declarar la funcion
        """
        if f_name not in self.function_table.table:
            # el cuadruplo inicial de la funcion
            quad = self.quad_counter + 1
            self.function_table.declare_function(f_name, f_type if f_type else self.var_type, quad)
            # asignar la funcion al stack
            self.set_function(f_name)
            return True
        return False

    def set_type(self, var_type: str) -> None:
        """modifica el ultimo tipo de dato definido"""
        self.var_type = var_type

    def set_function(self, name: str) -> None:
        """agrega una funcion al stack"""
        self.function.push(name)

    def create_quad(self, operation: Quadruple.OperationType, mem_location_1: str, mem_location_2, mem_result: str) -> int:
        """Genera un cuadruplo y lo agrega a la lista de cuadruplos. Regresa el numero de cuadruplo actual"""
        self.quadruples.append(Quadruple(operation, mem_location_1, mem_location_2, mem_result))
        return self.quad_counter

    def create_jump(self) -> None:
        """agrega un punto de salto para regresar en los goto"""
        self.jumpStack.push(self.quad_counter)

    def fill_quad(self, end: int = -1) -> None:
        """
        Funcion que llena un cuadruplo ubicado en el indice primero almacenado en el stack de saltos con el indice
        del cuadruplo proximo

        :param end: (opcional) posicion del salto
        :return: None
        """
        jump_index = end if end != -1 else self.jumpStack.pop()
        quad_index = self.quad_counter
        try:
            self.quadruples[jump_index].result = quad_index + 1
        except IndexError:
            print(f"Error accediendo indice {jump_index} de la lista de cuadruplos")

    def create_first_dim_access_quads(self):
        """
        Funcion que crea el cuadruplo de verificacion para el acceso de la primera dimension

        :return: None
        """
        var_dir = self.operands.top()
        var_type = self.types.top()

        if var_type != "int":
            print(f"Error. Indice debe ser de tipo entero")

        dim_context = self.dimensions.top()
        dim_var = self.get_variable(dim_context[0])
        first_dimension = avail.get_next_const("int", dim_var.dimensions[0].upper_bound)
        self.create_quad(Quadruple.OperationType.VER,
                         var_dir,
                         '',
                         first_dimension)

        if len(dim_var.dimensions) == 2:
            second_dimension = avail.get_next_const("int", dim_var.dimensions[1].m)
            self.operands.push(second_dimension)
            self.types.push("int")
            self.operations.push("*")
            self.create_operation_quad(["*"])

    def create_second_dim_access_quads(self):
        var_dir = self.operands.top()
        var_type = self.types.top()

        if var_type != "int":
            print(f"Error. Indice debe ser de tipo entero")

        dim_context = self.dimensions.top()
        dim_var = self.get_variable(dim_context[0])
        second_dimension = avail.get_next_const("int", dim_var.dimensions[1].upper_bound)
        self.create_quad(Quadruple.OperationType.VER,
                         var_dir,
                         '',
                         second_dimension)

        self.operations.push("+")
        self.create_operation_quad(["+"])

    def create_dimension_final_quads(self):
        """
        Funcion que genera el cuadruplo de suma
        :return:
        """
        aux_var = self.operands.pop()
        aux_type = self.types.pop()

        base = self.get_variable(self.dimensions.pop()[0])
        base_dir_const = avail.get_next_const("int", base.direction)

        pointer_dir = self.generate_temp("pointer")
        self.create_quad(
                Quadruple.OperationType.ADD,
                f"({aux_var})" if aux_type == "pointer" else aux_var,
                base_dir_const,
                str(pointer_dir))

        self.operands.push(pointer_dir)
        self.types.push("pointer")
        self.operations.pop()

    def create_operation_quad(self, operations: List[str]) -> None:
        """
        Funcion que genera un cuadruplo para las operaciones de formato (op, dir, dir, res). Se le pasa un arreglo de
        posibles operadores para realizar el proceso de creacion de cuadruplo para la operacion

        :param operations: lista de operaciones para validar con el el stack de operadores.
        :return: None
        """

        if not self.operations.top() in operations:
            return
        # extraer los operandos y sus tipos de los stacks
        right_operand = self.operands.pop()
        right_type = self.types.pop()

        left_operand = self.operands.pop()
        left_type = self.types.pop()

        operator = self.operations.pop()

        # calcular el tipo resultante
        try:
            resultant_type = self.semantic_cube.cubo[left_type][right_type][operator]
        except KeyError:
            resultant_type = None

        if resultant_type:
            # crear una variable temporal para almacenar el resultado
            result = avail.get_next_local(resultant_type, True, "")

            # generar el cuadruplo
            self.create_quad(Quadruple.get_operator_name(operator),
                             f"({left_operand})" if left_type == "pointer" else left_operand,
                             f"({right_operand})" if right_type == "pointer" else right_operand,
                             result)
            # agregar el resultado al stack de operadores y de tipos
            self.operands.push(result)
            self.types.push(resultant_type)
        else:
            print(f"Error de sintaxis. Type Error")

    def declare_variable(self, var_name: str, dimensions: [], is_global: bool) -> bool:
        """
        Funcion que declara una variable dentro del contexto de la funcion actual

        :param var_name: el nombre de la variable a crear
        :param dimensions: las dimensiones de la variable
        :param is_global: si la variable es global
        :return: si se logro declarar la variable
        """
        if is_global:
            var_direction = avail.get_next_global(self.var_type, False, var_name)
        else:
            var_direction = avail.get_next_local(self.var_type, False, var_name)

        if not dimensions:
            dimensions = []
        # generar un arreglo con los valores enteros de las dimensiones
        dims = [int(avail.get_val_from_dir(val)) for val in list(dimensions) if val is not None]

        # crear una variable y asignar el tamano respectivo al avail
        new_var = Variable(self.var_type, var_name, dims, var_direction)
        avail.set_size(new_var.type, new_var.size, is_global)
        # intentar declarar la variable
        if not self.function_table.declare_variable(self.function.top(), new_var):
            return False
        return True

    def is_variable_declared(self, var_name: str) -> bool:
        """Regresa si la vaariable ya esta declarada en el contexto actual"""
        return self.function_table.is_variable_declared(self.function.top(), var_name)

    def get_variable(self, var_name: str) -> Variable:
        """regresa la variable en el contexto actual"""
        return self.function_table.get_variable(self.function.top(), var_name)

    def get_dimensions(self, var_name: str) -> List[int]:
        """Regresa las dimensiones de la variable en forma de aarreglo de enteros"""
        return self.function_table.get_dimensions(self.function.top(), var_name)

    def get_function(self) -> Function:
        """Regresa la funcion del contexto actual"""
        return self.function_table.function(self.function.top())

    def end_function(self, quad: bool = True) -> None:
        """
        funcion que realiza el proceso de terminacion de una funcion. Elimina la funcion del contexto,
        genera el cuadruplo de END_FUNC, reinicia las variables locales del avail y calcula el tamano de la funcion
        en termino de variables y sus tipos

        :param quad: si se desea generar el cuadruplo de END_FUNC
        :return: None
        """
        function = self.get_function()
        function_name = self.function.pop()
        if quad:
            self.create_quad(Quadruple.OperationType.END_FUNC, "", "", "")
        temps = avail.reset_locals()
        self.function_table.erase_var_table(function_name)
        function.temps = temps

    def generate_temp(self, temp_type: str) -> int:
        """Genera una variable temporal"""
        if self.function.top() == "global":
            return avail.get_next_global(temp_type, True)
        else:
            return avail.get_next_local(temp_type, True)

    def __str__(self):
        return "({}, {})".format(self.function, self.var_type)
