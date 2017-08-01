def graph(**kwargs):
    x = kwargs["x"];
    if isinstance(x, str):
        x = list(map(int, x.split(",")))
    y = kwargs["y"];
    if isinstance(y, str):
        y = list(map(int, y.split(",")))
    title = xlab = ylab = "";
    plotmode = "x";
    if "lab" in kwargs:
        xlab, ylab = kwargs["lab"];
    if "title" in kwargs:
        title = kwargs["title"];
    if "pltmd" in kwargs:
        plotmode = kwargs["pltmd"];
    import matplotlib;
    matplotlib.use('Agg');
    import matplotlib.pyplot as plt;
    fig = plt.figure();
    sp = fig.add_subplot(111);
    sp.plot(x, y, plotmode);
    sp.set_title(title);
    sp.set_xlabel(xlab);
    sp.set_ylabel(ylab);
    from io import BytesIO;
    with BytesIO() as imgdata:
        fig.savefig(imgdata, format='png');
        imgdata.seek(0);
        del fig;
        return dict(datatype="image/png", data=imgdata.getvalue())