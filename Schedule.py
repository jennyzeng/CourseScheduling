class Schedule:
    """a schedule"""

    def __init__(self, widths):
        self.L = [[]]
        self.curWidths = [0]
        self.widths = widths  # maximum width for each layer

    def __len__(self):
        return len(self.L)

    def __str__(self):
        return "schedule: \n {s} \n curWidth: {curw} \n maxwidth:{mw} \n".format(s=self.L, curw=self.curWidths,
                                                                                 mw=self.widths)



    def clear_empty(self):
        while (not self.L[-1]) and (not self.curWidths[-1]):
            self.L.pop()
            self.curWidths.pop()

    def add_layer(self):
        self.L.append([])
        self.curWidths.append(0)

    def add_course(self, i, cid, c_units):
        """
        :param i: index of layer L_i
        :param cid: id of a course, that is, the key of a course in graph
        :param c_units: course units
        :return: None
        """
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
        return self.curWidths[i] + c_units <= self.max_width(i)