# Kaishi
Tool kit to accelerate the initial phases of exploratory data analysis.

## Brief Overview
The advent of deep learning provides opportunities to detect issues present in data that would otherwise be extremely difficult to detect algorithmically (unnatural image aspect ratios, subjectively similar data, etc.). Kaishi attempts to take advantage of this to help you get to know your data subjectively and intimately on the front end, thus saving time that would have been spent debugging later on. There are, of course, many standard tools built in as well (deduplication, artifact detection, merge operations, etc.) that can all be chained to provide powerful automated data engineering.

Two data types (images and tabular data) are currently implemented, but more (e.g. signals, video, etc.) will be added in future releases. A lot of functionality for new data types exists out of the box though, especially when it comes to file handling.

# Requirements
Python 3.6+

# Contributing
Some general guidelines to keep in mind when contributing
* Rely on convention as opposed to providing extensive configuration
* Don't invent features that _might_ be needed. If you've seen an issue more than once in the past or are presented with it in the future, feel free to add functionality and submit a PR.
* Try to follow a factory approach where possible

# Installation
To install (it will take a few secs to copy over the weights file(s)):
```
pip install -r requirements.txt
pip install .
```

# Quick Start
The only requirement to use Kaishi is that your dataset is a directory of files. It is first and foremost a discovery tool, and thus is not optimized for huge data sets. Try working with a subset to start exploring.

To run a simple image processing pipeline, try the below:
```
from kaishi.image.dataset import ImageDataset
imdata = ImageDataset('sample_images', recursive=True)
imdata.configure_pipeline(["FilterInvalidFileExtensions", "FilterDuplicateFiles"])
# You can also use imdata.configure_pipeline() without arguments to get guided input
imdata.file_report()
```

You will get command line output that looks like the below:
```
Current file list:
+---------------------------------------------+---------------------------------------------------------------------+--------+
|                  File Name                  |                               Children                              | Labels |
+---------------------------------------------+---------------------------------------------------------------------+--------+
|                real_near2.jpg               | {'duplicates': [this_is_a_directory/real_near2.jpg], 'similar': []} |   []   |
|                real_near1.jpg               | {'duplicates': [this_is_a_directory/real_near1.jpg], 'similar': []} |   []   |
|                  empty.jpg                  |        {'duplicates': [empty.jpeg, empty.bmp], 'similar': []}       |   []   |
|                real_same1.jpg               |           {'duplicates': [real_same2.jpg], 'similar': []}           |   []   |
| this_is_a_directory/image_rotated_right.jpg |                  {'duplicates': [], 'similar': []}                  |   []   |
|  this_is_a_directory/image_rotated_left.jpg |                  {'duplicates': [], 'similar': []}                  |   []   |
|   this_is_a_directory/image_rectified.jpeg  |                  {'duplicates': [], 'similar': []}                  |   []   |
|       documents/doc3_rotated_right.png      |                  {'duplicates': [], 'similar': []}                  |   []   |
|         documents/doc2_rectified.jpg        |                  {'duplicates': [], 'similar': []}                  |   []   |
|       documents/doc1_rotated_left.jpg       |                  {'duplicates': [], 'similar': []}                  |   []   |
+---------------------------------------------+---------------------------------------------------------------------+--------+
Filtered files:
+------------------------------------+-----------------------+
|             File Name              |     Filter Reason     |
+------------------------------------+-----------------------+
|          unsupported.gif           | unsupported_extension |
|               empty                | unsupported_extension |
| this_is_a_directory/real_near1.jpg |       duplicates      |
| this_is_a_directory/real_near2.jpg |       duplicates      |
|             empty.bmp              |       duplicates      |
|           real_same2.jpg           |       duplicates      |
|             empty.jpeg             |       duplicates      |
+------------------------------------+-----------------------+
```

Finally, you can save your modified datset in a new directory with the below command:
```
imd.save('output_directory')
```

This process is agnostic to the data type you have chosen. For instance:
```
from kaishi.tabular.dataset import TabularDataset
td = TabularDataset('sample_data', recursive=True)
td.configure_pipeline(['FilterDuplicateFiles'])
td.run_pipeline()
td.save('output_directory_tabular')
```

Some pipeline components are, of course, unique to a particular data type. To see which are available:
```
imd.get_pipeline_options()
# or td.get_pipeline_options()
```

# A note on pipeline components
Pipeline components are broken up into several distinct categories, and the classes that define them MUST begin with the correct keyword:
* `Filter*` - removes elements of a dataset
* `Transform*` - changes one or more data objects in some fundamental way
* `Labeler*` - creates labels for data objects without modifying the underlying data
* `Aggregator*` - combines data objects in some way (currently not implemented)
* `Sorter*` - reorders data objects in somw way (currently not implemented)

Look at how other pipeline components are implemented. Feel free to write your own, while following the below rules:
* Inherits from the `PipelineComponent` class
* Has a single initialization argument (a dataset object)
* Has a single `__call__` method with no arguments (this is where the dataset object is manipulated)

You can then enable usage of the component with your instantiated dataset object, e.g.:
```
from your_definition import YourNewComponent
imd.YourNewComponent = YourNewComponent
imd.configure_pipeline(['YourNewComponent'])
```

Finally, if the component needs special parameters, there must always be defaults defined as named arguments to a `.configure()` method. When `__init__` is called, this configure method will be initialized with the default arguments. A call to `.configure(...)` in the script that instantiated the component sets the parameters for the pipeline run.
_NOTE: `PipelineComponent` already has a `.configure()` method that warns that no arguments are configurable._
