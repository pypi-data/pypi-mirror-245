import matplotlib.pyplot as plt

def curves(listX, listY, listLabel, title, xLabel="X Axis", yLabel="Y Axis", width=10, height=6, xScale="log",
           yScale="log"):
    """Plot curve with your parameters.

        Parameters :
            listX (list): List of list, each sublist should contain x coordinates of every dot
            listY (list): List of list, each sublist should contain y coordinates of every dot
            listLabel (list) : List of string, label of each curve
            title (str) : Title of the plot
            xLabel (str) : Label of x axis (optional) (default : X Axis)
            yLabel (str) : Label of y axis (optional) (default : Y Axis)
            width (int) : Width of the plot (optional) (default : 10)
            height (int) : Height of the plot (optional) (default : 6)
            xScale (str) : Scale of x axis (optional) (linear, log, symlog, logit) (default : log)
            yScale (str) : Scale of y axis (optional) (linear, log, symlog, logit) (default : log)

        Return :
            None

        Assert :
            len(listX) == len(listY) == len(listLabel)
            len(listX[i]) == len(listY[i]) for i in range(len(listX))
    """
    assert len(listX) == len(listY) == len(listLabel), "listX, listY and listLabel must have the same length"
    assert all(len(listX[i]) == len(listY[i]) for i in range(len(listX))), "listX[i] and listY[i] must have the same length for all i"

    plt.figure(figsize=(width, height))

    for i in range(len(listX)):
        plt.plot(listX[i], listY[i], label=listLabel[i])

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    plt.xscale(xScale)
    plt.yscale(yScale)

    plt.title(title)
    plt.legend()
    plt.show()


xVal = [[10, 100, 1000, 10000, 100000],
          [10, 100, 1000, 10000, 100000, 1000000],
          [10, 100, 1000, 10000, 100000]]

yVal = [[57294, 607418, 6755705, 331559735, 33178671213],
          [45717, 299134, 1715546, 10415336, 157352093, 12800502882], [69268, 2490323, 5273649, 71921675, 3268629864]]
curvesLabel = ["HeapTree", "ArrayList", "HeapArray"]
name = 'Compare sort algorithms on random lists'
xLabel = 'List size'
yLabel = 'Execution time (nano seconds)'
xScale = "log"
yScale = "log"

curves(xVal, yVal, curvesLabel, name, xLabel, yLabel, xScale=xScale, yScale=yScale)