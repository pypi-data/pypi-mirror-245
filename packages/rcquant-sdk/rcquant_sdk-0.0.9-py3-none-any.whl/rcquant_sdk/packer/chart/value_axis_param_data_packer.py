from ...interface import IPacker


class ValueAxisParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [int(self._obj.PlotIndex), int(self._obj.ValueAxisID), int(self._obj.MaxTickNum), float(self._obj.Steps),
                str(self._obj.Format), int(self._obj.LabelTextLen), float(
                    self._obj.ValidMul), float(self._obj.PriceTick),
                int(self._obj.Precision)]

    def tuple_to_obj(self, t):
        if len(t) >= 9:
            self._obj.PlotIndex = t[0]
            self._obj.ValueAxisID = t[1]
            self._obj.MaxTickNum = t[2]
            self._obj.Steps = t[3]
            self._obj.Format = t[4]
            self._obj.LabelTextLen = t[5]
            self._obj.ValidMul = t[6]
            self._obj.PriceTick = t[7]
            self._obj.Precision = t[8]

            return True
        return False
