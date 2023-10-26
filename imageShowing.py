import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.image as mpimg
from tools import photoPathForId
from matplotlib.widgets import Button
import matplotlib.gridspec as gridspec


class ImagePlot():
    def __init__(self):
        self.current_index = 0
        self.image_paths = []
        self.labels = []
        self.fig = ""
        self.ax = ""
        self.gs = ""

imagePlot = ImagePlot()

def showBestMantas(data):
    imagePlot.current_index = 0

    print("Opening images in new plot - you must close the plot for the code to continue")
    handledMantas = []
    for sighting in data.sightings:
        if sighting.isManta and sighting.mantaIdWithUnknown not in handledMantas:
            handledMantas.append(sighting.mantaIdWithUnknown)
            imagePlot.image_paths.append(photoPathForId(data, sighting.bestPhotoId))
            imagePlot.labels.append(sighting.mantaIdWithUnknown)



    # # Create the figure and ImageGrid
    # imagePlot.fig, imagePlot.ax = plt.subplots(figsize=(8, 6))
    # display_current_image(imagePlot.current_index)

    # Create the figure and a gridspec layout
    imagePlot.fig = plt.figure(figsize=(10, 8))
    imagePlot.gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])

    print(imagePlot.labels)
    # Create navigation buttons

    # Create separate axes for navigation buttons
    ax_buttons = plt.subplot(imagePlot.gs[1])

    ax_prev = plt.axes([0.3, 0.2, 0.1, 0.05])
    ax_next = plt.axes([0.6, 0.2, 0.1, 0.05])


    # ax_prev = plt.subplot(imagePlot.gs[1])
    # ax_next = plt.subplot(imagePlot.gs[1])

    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')

    btn_prev.on_clicked(prev_image)
    btn_next.on_clicked(next_image)

    # Create the axis for displaying images
    imagePlot.ax = plt.subplot(imagePlot.gs[0])
    display_current_image(imagePlot.current_index)
    
    plt.show()

# Create a function to display the current image
def display_current_image(index):
    print(f"Index {index}")
    print(f"Display image for {imagePlot.labels[index]} with path {imagePlot.image_paths[index]}")
    imagePlot.ax.clear()
    img = mpimg.imread(imagePlot.image_paths[index])
    imagePlot.ax.imshow(img)
    imagePlot.ax.set_title(imagePlot.labels[index])
    imagePlot.fig.canvas.draw()
    imagePlot.fig.canvas.flush_events()


# Define functions for navigation
def next_image(event):
    print("next image")
    imagePlot.current_index = (imagePlot.current_index + 1) % len(imagePlot.image_paths)
    display_current_image(imagePlot.current_index)

def prev_image(event):
    print("prev image")
    imagePlot.current_index = (imagePlot.current_index - 1) % len(imagePlot.image_paths)
    display_current_image(imagePlot.current_index)

def openAllBestMantaImages(data):
    print("Opening images in new plot - you must close the plot for the code to continue")
    image_paths = []
    labels = []
    handledMantas = []
    for sighting in data.sightings:
        if sighting.isManta and sighting.mantaIdWithUnknown not in handledMantas:
            handledMantas.append(sighting.mantaIdWithUnknown)
            image_paths.append(photoPathForId(data, sighting.bestPhotoId))
            labels.append(sighting.mantaIdWithUnknown)

    # Create a subplot grid
    num_images = len(image_paths)
    num_cols = 2  # You can adjust the number of columns as per your preference
    num_rows = (num_images + num_cols - 1) // num_cols

    # Create the subplots and display images with labels
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
    axes = axes.flatten()  # Convert the 2D array of axes to a 1D array
    for i, (image_path, label) in enumerate(zip(image_paths, labels)):
        ax = axes[i]

        # Load and display the image
        img = mpimg.imread(image_path)
        ax.imshow(img)
        ax.set_title(label)
        ax.axis('off')  # Turn off axis labels

    # Hide any remaining empty subplots
    for i in range(num_images, num_rows * num_cols):
        fig.delaxes(axes[i])

    # Adjust subplot layout
    plt.tight_layout()

    # Show the plot
    plt.show()