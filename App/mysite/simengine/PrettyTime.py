def prettyTime(startTime,timestep):
        h, m = divmod(timestep, 60)
        sh,sm = divmod(startTime, 60)
        return "%d:%02d" % (h + sh, m + sm)
