import sys

import pandas as pd
import matplotlib.pyplot as plt


class NoaaReport:
    """Reads noaa report.
    """

    def __init__(self, filename):
        self._filename = filename
        self._data = []
        self.df = None

    def __check_data(self):
        """Checks if the data has already been saved. """
        if len(self._data):
            return True

        self._read_data()

    def _read_data(self):
        """Reads the noaa report.
        """
        with open(self._filename) as _file:
            for line in _file.readlines():
                sep = line.split()

                try:
                    if (not sep[0].startswith(":") and
                            not sep[0].startswith("#")):

                        self._data.append(sep)
                except IndexError:
                    pass

            for event in self._data:
                if event[1] == "+":
                    event[0] += " +"
                    del event[1]

    def set_Qs(self):
        """TODO """
        self.__check_data()
        Qs = []
        for info in self._data:
            if len(info[5]) == 1:
                Qs.append(info[5])
            else:
                Qs.append("None")
        return Qs

    def set_observatories(self):
        """TODO """
        self.__check_data()
        index = 0
        observatories = []
        while index < len(self._data):
            if len(self._data[index][4]) == 3:
                observatories.append(self._data[index][4])
                index += 1
            else:
                del self._data[index]

        return observatories

    def set_particulars(self):
        """TODO """
        self.__check_data()
        particulars = []
        for info in self._data:
            try:
                last_index = len(info) - 1
                if info[last_index].isdigit() and len(info[last_index]) == 4:
                    if len(info) > 10:
                        particula = (info[last_index - 2] + " " +
                                     info[last_index - 1])
                    else:
                        particula = info[last_index - 1]
                else:
                    if len(info) > 9:
                        particula = (info[last_index - 1] + " " +
                                     info[last_index])
                    else:
                        particula = info[last_index]

                particulars.append(particula)
            except IndexError:
                particulars.append("None")

        return particulars

    def set_regions(self):
        """TODO """
        #
        #
        #
        self.__check_data()
        reg = []
        for info in self._data:
            try:
                last_index = len(info) - 1
                if info[last_index].isdigit() and len(info[last_index]) == 4:
                    reg.append(info[last_index])
                else:
                    reg.append("None")
            except IndexError:
                reg.append("None")
        
        return reg

    def set_event(self):
        """TODO """
        self.__check_data()
        return [i[0] for i in self._data]

    def set_begin(self):
        """TODO """
        self.__check_data()
        return [i[1] for i in self._data]

    def set_max(self):
        """TODO """
        self.__check_data()
        return [i[2] for i in self._data]

    def set_end(self):
        """TODO """
        self.__check_data()
        return [i[3] for i in self._data]

    def set_type(self):
        """TODO """
        self.__check_data()
        return [i[6] for i in self._data]

    def set_freq(self):
        """TODO """
        self.__check_data()
        return [i[7] for i in self._data]

    def set_final_data(self):
        """TODO """
        self.__check_data()

        # observatories must be declared first, because it changes the
        # data list.
        final_data = {
            "obs": self.set_observatories(),
            "event": self.set_event(),
            "begin": self.set_begin(),
            "max": self.set_max(),
            "end": self.set_end(),
            "Q": self.set_Qs(),
            "type": self.set_type(),
            "loc/freq": self.set_freq(),
            "particulars": self.set_particulars(),
            "reg": self.set_regions()
        }

        columns = ["event", "begin", "max",
                   "end", "obs", "Q", "type",
                   "loc/freq", "particulars", "reg"]

        self.df = pd.DataFrame(final_data, columns=columns)
        print(self.df)

    def get_active_region(self, start_time, end_time):
        """Returns registered active region of a certain time range.
        
        Arguments:
            start_time {str} -- event's start time.
            end_time {str} -- event's end time.
        """

        start_time = str(start_time)
        end_time= str(end_time)
        start_time = start_time[11:16].replace(":", "")
        end_time = end_time[11:16].replace(":", "")
        # ar = []
        freqs = []
        parts = []

        for i in range(0, len(self.df)):
            if (self.df["type"][i] == "XRA" and
                    self.df["particulars"][i].startswith("X")):
                sav = i
                # print(self.df.loc[i])

            if (self.df["type"][i] == "RBR" and self.df["begin"][i] > "1153"
                    and self.df["begin"][i] < "1300"):
                print(self.df["begin"][i])
                print(self.df["loc/freq"][i])
                freqs.append(self.df["loc/freq"][i])
                if self.df["particulars"][i].split()[0].isnumeric():
                    print(self.df["particulars"][i].split()[0])
                    parts.append(self.df["particulars"][i].split()[0])

                print("\n")

        print(freqs)
        print(parts)
        plt.plot(freqs, parts)

        """
        if int(self.df["end"][i]) < 10:
            continue
        if (int(self.df["begin"][i]) >= int(start_time)
                and int(self.df["end"][i]) <= int(end_time)):
            # print(self.df.loc[i])
            ar.append(self.df["reg"][i])
        """

        # print(self.df.loc[31])


if __name__ == "__main__":
    report = NoaaReport(sys.argv[1])
    report.set_final_data()
    report.get_active_region(
        "2002-04-09 12:44:43.999440+00:00",
        "2002-04-09 13:09:58.001280+00:00")