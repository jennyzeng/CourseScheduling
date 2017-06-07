"""
A schedule that consists of a few layers (quarters).
"""

__author__ = "Jenny Zeng"
__email__ = "jennyzengzzh@gmail.com"


class Schedule:
    """a schedule"""

    def __init__(self, widths):
        self.L = [[]]
        self.curWidths = [0]
        self.widths = widths  # maximum width for each layer

    def __len__(self):
        return len(self.L)

    def __str__(self):
        output = ""
        for index, layer in enumerate(self.L):
            output += "\nlayer: {index}, with width {curw} and max {wmax}\n".format(
                index=index, curw=self.curWidths[index], wmax=self.max_width(index))
            output += "; ".join([str(cid) for cid in layer]) + "\n"
        return output

    def clear_empty(self):
        """
        clear empty layers at tops until the top layer is a non-empty layer
        :return:
        """
        while (not self.L[-1]) and (not self.curWidths[-1]):
            self.L.pop()
            self.curWidths.pop()

    def add_layer(self):
        """
        add a empty layer above the top layer, and mark its curWidth to be 0
        """
        self.L.append([])
        self.curWidths.append(0)

    def add_course(self, i, cid, c_units):
        """
        :param i: index of layer L_i
        :param cid: id of a course, that is, the key of a course in graph
        :param c_units: course units
        :return: None
        """
        while i >= len(self.L):
            self.add_layer()
        self.L[i].append(cid)
        self.curWidths[i] += c_units

    def max_width(self, i):
        """
        :param i: index for layer L_i
        :return: max_width for layer L_i
        """
        if i in self.widths:
            return self.widths[i]
        else:
            return self.widths["else"]

    def layer_is_full(self, i, c_units):
        """
        :param i: index for layer L_i
        :param c_units: new course units
        :return: true if adding this course would make L_i exceed
                its maximum width
        """

        return (i < len(self.L)) and (self.curWidths[i] + c_units > self.max_width(i))
