import matplotlib
import matplotlib.pyplot as plt
import astropy.visualization

def visualize_image(array, vmin=None, vmax=None, scale=None, percentile=None, lower_percentile=None, upper_percentile=None):
    if scale is not None:
        if scale=='zscale':
            vis=astropy.visualization.ZScaleInterval(nsamples=1000, contrast=0.25, max_reject=0.5, 
                                             min_npixels=5, krej=2.5, max_iterations=5)
        elif scale=='minmax': vis=astropy.visualization.MinMaxInterval()
        if percentile is not None: vis=astropy.visualization.PercentileInterval(percentile)
        if (lower_percentile is not None )& (upper_percentile is not None):
                vis=astropy.visualization.AsymmetricPercentileInterval(lower_percentile, upper_percentile )       
        vmin,vmax=vis.get_limits(array)
    print("using vmin, vmax: %.3f, %.3f"%(vmin,vmax))
    fig = plt.figure(dpi=200)
    ax = fig.subplots()
    ax.axis('off')
    #ax.axes.xaxis.set_visible(False)
    #ax.axes.yaxis.set_visible(False)
    ax.imshow( array , cmap = plt.cm.gray , vmin = vmin , vmax =vmax , origin = 'lower')
    #ax.grid( color = 'gray') 