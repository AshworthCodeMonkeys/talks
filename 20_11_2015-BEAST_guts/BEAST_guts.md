# BEAST

## What is it?
**B**ayesian **E**volutionary **A**nalysis by **S**ampling **T**rees is a cross-platform software package for Bayesian phylogenetic analysis of molecular sequences using Markov chain Monte Carlo (MCMC).
It is implemented in [JAVA](http://docs.oracle.com/javase/8/) and depends on JRE version 1.6 or higher to run.

Programs distributed in the BEAST "bundle":
- [BEAST mcmc](http://beast.bio.ed.ac.uk/BEAST): Runs the MCMC from XML configuration files. Is the heart of the BEAST framework;
- [BEAUti](http://beast.bio.ed.ac.uk/BEAUti): an user-friendly GUI for creating input (configuration) XML files to run BEAST;
- [LogCombiner](http://beast.bio.ed.ac.uk/LogCombiner): a program (GUI) to combine log and tree files from multiple runs of BEAST;
- [TreeAnnotator](http://beast.bio.ed.ac.uk/TreeAnnotator): program for summarising the information in a sample of trees produced by BEAST.

The BEAST family also has two other honorary members:
- [Tracer](http://beast.bio.ed.ac.uk/Tracer): graphical program for analysing results from MCMC programs such as BEAST and [MrBayes](http://mrbayes.sourceforge.net/);
- [FigTree](http://beast.bio.ed.ac.uk/FigTree): A program for viewing trees including summary information produced by TreeAnnotator, a.k.a, "annotated" trees.

In the [development repository](https://github.com/beast-dev/beast-mcmc) you will find the current ~~bug-prone~~  bleeding-edge version of BEAST.
Supposing you want the dev version:
```bash
user@machine:~$ git clone git@github.com:beast-dev/beast-mcmc.git
user@machine:~/beast-mcmc$ cd beast-mcmc/
user@machine:~/beast-mcmc$ ant
```
will build both `beast.jar` and `beauti.jar` in beast-mcmc/build/dist/.

This is what we informally call "BEAST 1", the original BEAST. 

[Alexei Drummond](http://compevol.auckland.ac.nz/dr-alexei-drummond/) and his team have developed [BEAST2](http://beast2.org/) that features a more modular, plugin-based architecture where users can contribute plugins implementing a plethora of phylogenetic models.
The development repo for BEAST2 sits [here](https://github.com/compevol/beast2).

For doubts and general troubleshooting (after RTFM), see the [user group](https://groups.google.com/forum/#!forum/beast-users).

### BEAGLE

Likelihood computations are costly. To address this, Daniel Ayres and peers have written the **B**road-platform **E**volutionary **A**nalysis **G**eneral **L**ikelihood **E**valuator (BEAGLE), a C library that provides "fine-scale parallelization while minimizing data transfer and memory copy overhead" (see [paper](http://sysbio.oxfordjournals.org/content/61/1/170)).
BEAGLE brings substantial speed-ups in likelihood computation by efficiently using multicore CPUs and modern bazillion-core graphical processing units (GPUs).
BEAGLE is compatible with a range of phylogenetic software, such as BEAST, MrBayes, [PhyML](), and [Garli]().
The gain in speed is so significant that most complex models in BEAST, such as phylogeography,  now depend exclusively on BEAGLE to run.  See this [post](http://francoismichonneau.net/2014/05/how-to-install-beagle-on-ubuntu/) for a nice guide on how to get BEAGLE up and running.

### Using BEAST
if you want to look at the options
```bash
user@machine:~$ java -Xms64m -Xmx4096m -jar /path/to/beast -help
```
A typical run would look something like this 
```bash
user@machine:~$ java -Xms64m -Xmx4096m -Djava.library.path=/path/to/beagle -jar /path/to/beast -beagle_SSE -threads 8 input.xml
```

## How does it work?

BEAST feeds on ~~souls~~ XML input files that are supposed specify everything you need to run MCMC and get a posterior distribution for your parameters:
- Data!
- Likelihoods (i.e, models);
- Priors;
- Operators;
- Number of iterations, sampling frequency and auto-optimisation options.

Having everything in the same place makes it easy to share and reproduce analyses.

Now, what the heck is an "operator"?

In BEAST, we name Operators all of the MCMC **proposals**.
Example: how do you propose a new tree topology within the chain? Use a SubTreeSlide, NarrowExchange or Wilson-Balding operator.
Each operator is given a **weight**, that tells BEAST how often to perform that particular proposal.
In order to achieve better efficiency, some proposals in BEAST are **tunable**, which means their width (variance) can be adjusted such that we attain a certain acceptance probabiliy (usually around 0.234). We call this auto-optimise and it comes in two flavours: "default" and "log", which differ in how they relate proposal variance and acceptance probability.

### General architecture

Being coded in JAVA, BEAST is naturally sort of modular. The wide array of different necessary components to allow the kind of model complexity BEAST offers, however, calls for some more deliberate modularity in order to avoid conflicts and broken dependencies. BEAST2, for instance, capitalises on the general routines developed for BEAST but has a much stronger focus on modularity.

Ok, enough with the babbling. Let's take a look at BEAST's internal structure, borrowing ~~very~~ heavily from the [developer notes](https://code.google.com/p/beast-mcmc/wiki/DeveloperNotes).

In order to avoid circular dependencies between packages, certain packages are intended as global utility classes (``feel free to add stuff to them but consider whether they may be useful to other classes``):
- ``dr.maths`` / ``dr.stats`` / ``dr.utils`` are low level utility packages and should have no dependencies on the packages below;
- ``dr.inference`` comprises generic MCMC routines and should have no dependencies on the _biological_ packages (``dr.evolution`` and ``dr.evomodel``). Notably, things like **priors**, **operators** are generic ones that work on continuous parameters not biology specific ones;
-  ``dr.evolution`` is basic evolutionary stuff and should have no dependencies on ``dr.evomodel`` or ``dr.inference``;
-  ``dr.evomodel`` is where all BEAST-specific stuff should go - this ties together the biology in ``dr.evolution`` into the inference engine in ``dr.inference``.

**~~Plugins~~**

If you're developing a whole new set of classes implementing a particular model, it is probabiliy desirable to "package" them together rather than distribute classes all over the place. Your best bet is to create all of your stuff inside ``dr.evomodel``. This was the germ of the plugin-based architecture of BEAST2, that allowed a range of model extensions to be [developed](http://beast2.org/beast-features/).

**Parsers**
- From now, any parser not ready for release should stay in development_parser.properties. Once it is ready for release, it should be moved into release parser.properties.
-  Any parser has to be implemented by an individual java class extended from ``AbstractXMLObjectParser`` and named by model name + Parser. If there are multi-parsers referring to one model class, they can be included in one parser class and each parser has its own inner class extended from ``AbstractXMLObjectParser``.
-  Model in dr.evolution = parser in ``dr.evoxml``,  model in ``dr.evomodel`` = parser in ``dr.evomodelxml``, model in ``dr.inference`` = parser in ``dr.inferencexml``.

## The XML configuration file format 

Now that we ~~kinda~~ know how BEAST works in the inside, let's talk about one of the most important features of BEAST: its E**X**tensible **M**arkup **L**anguage ([XML](https://en.wikipedia.org/wiki/XML)) input file specification.
Knowing your way around the XML syntax is important because the graphical utility for building XMLs is not nearly exhaustive. Thus, many of the interesting models are only available through manually editing the XMLs. 
First, let's look at a [BEAUti-constructed XML](https://github.com/AshworthCodeMonkeys/talks/blob/master/20_11_2015-BEAST_guts/dengue_example.xml). Now let's mess round a bit.

Suppose we want a Gamma distribution for the clock model, that is, we want to model the among-branch variation with a Gamma distribution rather than, say, a lognormal.

We would then need to change 

```xml
<!-- The uncorrelated relaxed clock (Drummond, Ho, Phillips & Rambaut (2006) PLoS Biology 4, e88 )-->
	<discretizedBranchRates id="branchRates">
		<treeModel idref="treeModel"/>
		<distribution>
			<logNormalDistributionModel meanInRealSpace="true">
				<mean>
					<parameter id="ucld.mean" value="0.001" lower="0.0"/>
				</mean>
				<stdev>
					<parameter id="ucld.stdev" value="0.3333333333333333" lower="0.0"/>
				</stdev>
			</logNormalDistributionModel>
		</distribution>
		<rateCategories>
			<parameter id="branchRates.categories"/>
		</rateCategories>
	</discretizedBranchRates>
```
with something like

```xml
	<!-- The uncorrelated  Gamma relaxed clock -->
	<discretizedBranchRates id="branchRates">
		<treeModel idref="treeModel"/>
		<distribution>
			<gammaDistributionModel offset="0.0">
				<shape>
					<parameter id="ucg.shape" value="1.0" lower="0.0"/>
				</shape>
				<scale>
					<parameter id="ucg.scale" value="0.001" lower="0.0"/>
				</scale>
			</gammaDistributionModel>
		</distribution>
		<rateCategories>
			<parameter id="branchRates.categories"/>
		</rateCategories>
```
Of course, this calls for changes in the operators, with
```xml
...
<scaleOperator scaleFactor="0.75" weight="3">
	<parameter idref="ucld.mean"/>
</scaleOperator>
<scaleOperator scaleFactor="0.75" weight="3">
	<parameter idref="ucld.stdev"/>
</scaleOperator>
...
```
becoming 
```xml
...
<scaleOperator scaleFactor="0.75" weight="3">
	<parameter idref="ucg.shape"/>
</scaleOperator>
<scaleOperator scaleFactor="0.75" weight="3">
	<parameter idref="ucg.scale"/>
</scaleOperator>
...
```
Further adjustments to the "priors" and "log" blocks would follow in a similar fashion.
This is what I would call the _trivial_ extensibility of BEAST. Let's now look at a slightly less trivial way of extending BEAST.

## Developing stuff for BEAST: an example
Imagine this [Andrew Rambaut](http://tree.bio.ed.ac.uk/people/arambaut/) guy wants to contribute a new tree proposal (move) to BEAST. 
Suppose that for some twisted reason the name of such move is ``SubtreeJump``.
Following the guidelines seen above when we visited the [developer notes](https://code.google.com/p/beast-mcmc/wiki/DeveloperNotes) we will place our new class ``SubTreeJumpOperator.java`` inside ``dr.evomodel.operators``.
The first lines of which would look something like
```java
package dr.evomodel.operators;

import dr.evolution.tree.NodeRef;
import dr.evolution.tree.Tree;
import dr.evomodel.tree.TreeModel;
import dr.evomodelxml.operators.SubtreeJumpOperatorParser;
import dr.inference.operators.*;
import dr.math.MathUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * Implements the Subtree Jump move.
 * @author Andrew Rambaut
 * @version $Id$
 */
public class SubtreeJumpOperator extends AbstractTreeOperator implements CoercableMCMCOperator {
...
}
```
Now, we need to write an XML parser for the new operator, to take in the specs it needs, in this case ``size`` and ``weight``.
This parser class, unsurprisingly called ``SubtreeJumpOperatorParser.java`` is to be placed  in ``dr.evomodelxml.operators`` and looks like this 
```java
package dr.evomodelxml.operators;

import dr.evomodel.operators.SubtreeJumpOperator;
import dr.evomodel.operators.SubtreeSlideOperator;
import dr.evomodel.tree.TreeModel;
import dr.inference.operators.CoercableMCMCOperator;
import dr.inference.operators.CoercionMode;
import dr.inference.operators.MCMCOperator;
import dr.xml.*;

public class SubtreeJumpOperatorParser extends AbstractXMLObjectParser {

    public static final String SUBTREE_JUMP = "subtreeJump";

    public String getParserName() {
        return SUBTREE_JUMP;
    }
   ...
}   
```
So in the end, one can just add 
```xml
<subtreeJump  size="1.0" weight="36">
    <treeModel idref="treeModel"/>
</subtreeJump>
```
to their XML to use the new operator.

## References
- BEAST: papers [1](http://www.biomedcentral.com/1471-2148/7/214) and [2](http://mbe.oxfordjournals.org/content/29/8/1969);
- BEAGLE: [paper](http://sysbio.oxfordjournals.org/content/61/1/170)
- BEAST2: [paper](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003537)
