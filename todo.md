# To Do List

This todo list is intended for the development team at Penn State's TLT. We'll be using this page to monitor and assess tasks in the development of the SKTimeline. For anyone observing the development of the project, this page might serve as a guide to our development and future directions.

The goal of the next few months of development will be to use the Python API wrappers to draw data from Twitter, Slack, and Github into a unified JSON file. The JSON file must be compatible with the [TimelineJS](https://timeline.knightlab.com) format available [here](https://timeline.knightlab.com/docs/json-format.html). Once we are drawing data down in real time and updating each users JSON file, we will need to build an <iframe> generator that will render the timeline for each user outside the platform. The Github page for [TimelineJS](https://github.com/NUKnightLab) provides all the code and examples needed for this.
