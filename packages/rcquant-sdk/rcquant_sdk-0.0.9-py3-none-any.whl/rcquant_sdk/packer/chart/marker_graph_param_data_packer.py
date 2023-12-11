from ...interface import IPacker


class MarkerGraphParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [str(self._obj.ID), str(self._obj.Name), int(self._obj.PlotIndex), int(self._obj.ValueAxisID),
                str(self._obj.Text), str(self._obj.TextColor), int(self._obj.TextVAlign), int(self._obj.TextHAlign),
                int(self._obj.Orientation), int(self._obj.LineDirec), int(self._obj.LineWidth), int(self._obj.LineStyle),
                str(self._obj.LineColor), float(self._obj.Key), float(self._obj.Value), int(self._obj.MillTimeSpan),
                bool(self._obj.JoinValueAxis), dict(self._obj.UserData)]

    def tuple_to_obj(self, t):
        if len(t) >= 18:
            self._obj.ID = t[0]
            self._obj.Name = t[1]
            self._obj.PlotIndex = t[2]
            self._obj.ValueAxisID = t[3]
            self._obj.Text = t[4]
            self._obj.TextColor = t[5]
            self._obj.TextVAlign = t[6]
            self._obj.TextHAlign = t[7]
            self._obj.Orientation = t[8]
            self._obj.LineDirec = t[9]
            self._obj.LineWidth = t[10]
            self._obj.LineStyle = t[11]
            self._obj.LineColor = t[12]
            self._obj.Key = t[13]
            self._obj.Value = t[14]
            self._obj.MillTimeSpan = t[15]
            self._obj.JoinValueAxis = t[16]
            self._obj.UserData = t[17]

            return True
        return False
