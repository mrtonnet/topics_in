* Draft: 2020-10-08 (Thu)

# Ablation Study

[What is an ablation study? And is there a systematic way to perform it?](https://stats.stackexchange.com/questions/380040/what-is-an-ablation-study-and-is-there-a-systematic-way-to-perform-it), StackExchange

> The term "ablation study" is often used in the context of neural networks, especially relatiavely complex ones such as R-CNNs. The idea is to learn about the network by removing parts of it and studying it's performance. In the context of linear regression that you propose, ablation doesn't really make sense - it would turn into a kind of backwards stepwise variable selection procedure. – [Robert Long](https://stats.stackexchange.com/users/7486/robert-long) [Dec 3 '18 at 10:14](https://stats.stackexchange.com/questions/380040/what-is-an-ablation-study-and-is-there-a-systematic-way-to-perform-it#comment714411_380040)

> The links below also provides helpuful infos on ablation analysis [overview](http://www.cs.ubc.ca/labs/beta/Projects/Ablation/) **and** [discussion on Ablation analysis](https://tinyurl.com/y3k3cy5s) – [iun1x](https://stats.stackexchange.com/users/244241/iun1x) [Oct 4 at 2:07](https://stats.stackexchange.com/questions/380040/what-is-an-ablation-study-and-is-there-a-systematic-way-to-perform-it#comment905469_380040) 

> The original meaning of “Ablation” is the [surgical removal of body tissue](https://www.dictionary.com/browse/ablation). The term “Ablation study” has its roots in the field of experimental neuropsychology of the 1960s and 1970s, where parts of animals’ brains were removed to study the effect that this had on their behaviour.
>
> In the context of machine learning, and especially complex deep neural networks, “ablation study” has been adopted to describe a procedure where certain parts of the network are removed, in order to gain a better understanding of the network’s behaviour.
>
> The term has received attention since a [tweet by Francois Chollet](https://twitter.com/fchollet/status/1012721582148550662?lang=en), primary author of the Keras deep learning framework, in June 2018:
>
> > Ablation studies are crucial for deep learning research -- can't stress this enough. Understanding causality in your system is the most straightforward way to generate reliable knowledge (the goal of any research). And ablation is a very low-effort way to look into causality.
> >
> > If you take any complicated deep learning experimental setup, chances are you can remove a few modules (or replace some trained features with random ones) with no loss of performance. Get rid of the noise in the research process: do ablation studies.
> >
> > Can't fully understand your system? Many moving parts? Want to make sure the reason it's working is really related to your hypothesis? Try removing stuff. Spend at least ~10% of your experimentation time on an honest effort to disprove your thesis.
>
> As an example, [Girshick and colleagues (2014)](https://arxiv.org/pdf/1311.2524.pdf) describe an object detection system that consists of three “modules”: The first proposes regions of an image within which to search for an object using the Selective Search algorithm ([Uijlings and colleagues 2012](https://staff.fnwi.uva.nl/th.gevers/pub/GeversIJCV2013.pdf)), which feeds in to a large convolutional neural network (with 5 convolutional layers and 2 fully connected layers) that performs feature extraction, which in turn feeds into a set of support vector machines for classification. In order to better understand the system, the authors performed an ablation study where different parts of the system were removed - for instance removing one or both of the fully connected layers of the CNN resulted in surprisingly little performance loss, which allowed the authors to conclude
>
> > Much of the CNN’s representational power comes from its convolutional layers, rather than from the much larger densely connected layers.
>
> The OP asks for details of /how/ to perform an ablation study, and for comprehensive references. I don't believe there is a "one size fits all" answer to this. Metrics are likely to differ, depending on the application and types of model. If we narrow the problem down simply to one deep neural network then it is relatively straight forward to see that we can remove layers in a principled way and explore how this changes the performance of the network. Beyond this, in practice, every situation is different and in the world of large complex machine learning applications, this will mean that a unique approach is likely to be needed for each situation.
>
> In the context of the example in the OP - linear regression - an ablation study does not make sense, because all that can be "removed" from a linear regression model are some of the predictors. Doing this in a "principled" fashion is simply a reverse stepwise selection procedure, which is generally frowned upon - see [here](https://andrewgelman.com/2014/06/02/hate-stepwise-regression/), [here](https://www.stata.com/support/faqs/statistics/stepwise-regression-problems/) and [here](https://stats.stackexchange.com/questions/20836/algorithms-for-automatic-model-selection/20856#20856) for details. A regularization procedure such as the Lasso, is a much better option for linear regression.
>
> Refs:
>
> Girshick, R., Donahue, J., Darrell, T. and Malik, J., 2014. Rich feature hierarchies for accurate object detection and semantic segmentation. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 580-587).
>
> Uijlings, J.R., Van De Sande, K.E., Gevers, T. and Smeulders, A.W., 2013. Selective search for object recognition. International journal of computer vision, 104(2), pp.154-171.



## Further Readings

TO-READ

* Ablation Study > Overview, http://www.cs.ubc.ca/labs/beta/Projects/Ablation/
* [In the context of deep learning, what is an ablation study?](https://www.quora.com/In-the-context-of-deep-learning-what-is-an-ablation-study#:~:text=An%20ablation%20study%20is%20where,important%20for%20human%20image%20recognition.), Quora
* [ablation study가 뭐냐 대체?](https://study-grow.tistory.com/37)



