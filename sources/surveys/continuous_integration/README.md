

## Build Automation

[Build automation](https://en.wikipedia.org/wiki/Build_automation) is the process of automating the creation of a [software build](https://en.wikipedia.org/wiki/Software_build) and the associated processes including:

* [compiling](https://en.wikipedia.org/wiki/Compiling) computer [source code](https://en.wikipedia.org/wiki/Source_code) into [binary code](https://en.wikipedia.org/wiki/Binary_code),
* [packaging](https://en.wikipedia.org/wiki/Software_package_(installation)) [binary code](https://en.wikipedia.org/wiki/Binary_code), and
* running [automated tests](https://en.wikipedia.org/wiki/Test_automation).

There are two general categories of tools:

* Build-automation utility
* Build-automation servers
  * Server types
    * On-demand automation (Build server)
    * Scheduled automation (Continuous Integration server or CI server)
    * Triggered automation (CI server)

* On-demand automation such as a user running a script at the command line

* Scheduled automation such as a continuous integration server running a nightly build
* Triggered automation such as a continuous integration server running a build on every commit to a version-control system.

## Build Automation Tool

[Apache Ant](https://ant.apache.org/) is a software tool for automating software build processes which originated from the [Apache Tomcat](https://en.wikipedia.org/wiki/Apache_Tomcat) project in early 2000. It was a replacement for the Make build tool of Unix, and was created due to a number of problems with Unix's make.
Languages used: XML, Java

[Apache Ant](https://en.wikipedia.org/wiki/Apache_Ant), Wikipedia

## "merge hell", or "integration hell"

The longer development continues on a branch without merging back to the mainline, the greater the risk of multiple integration conflicts and failures when the developer branch is eventually merged back. When developers submit code to the [source code repository](https://en.wikipedia.org/wiki/Source_code_repository) they must first update their code to reflect the changes in the repository since they took their copy. The more changes the repository contains, the more work developers must do before submitting their own changes.

Eventually, the repository may become so different from the developers' baselines that they enter what is sometimes referred to as "***merge hell***" or "***integration hell***" where the time it takes to integrate exceeds the time it took to make their original changes.

Source: [Continuous Integration (CI)](https://en.wikipedia.org/wiki/Continuous_integration)

## [Continuous Integration (CI)](https://en.wikipedia.org/wiki/Continuous_integration)

In [software engineering](https://en.wikipedia.org/wiki/Software_engineering), **continuous integration** (**CI**) is the practice of merging all developers' working copies to a shared [mainline](https://en.wikipedia.org/wiki/Trunk_(software)) several times a day.[[1\]](https://en.wikipedia.org/wiki/Continuous_integration#cite_note-martinfowler-1) [Grady Booch](https://en.wikipedia.org/wiki/Grady_Booch) first proposed the term CI in [his 1991 method](https://en.wikipedia.org/wiki/Booch_method),[[2\]](https://en.wikipedia.org/wiki/Continuous_integration#cite_note-2) although he did not advocate integrating several times a day. [Extreme programming](https://en.wikipedia.org/wiki/Extreme_programming) (XP) adopted the concept of CI and did advocate integrating more than once per day – perhaps as many as tens of times per day.[[3\]](https://en.wikipedia.org/wiki/Continuous_integration#cite_note-3)

### Workflows

#### Run tests locally

CI is intended to be used in combination with automated unit tests written through the practices of [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development). This is done by running and passing all unit tests in the developer's local [environment](https://en.wikipedia.org/wiki/Deployment_environment) before committing to the mainline. This helps avoid one developer's work-in-progress breaking another developer's copy. Where necessary, partially complete features can be disabled before committing, using [feature toggles](https://en.wikipedia.org/wiki/Feature_toggle) for instance.

#### Build servers

A build server compiles the code periodically or even after every commit and reports the results to the developers. In most cases, a build server also runs the unit tests. The use of build servers had been introduced by the XP community but nowadays, many organisations have adopted CI without adopting all of XP.

#### Quality control

In addition to automated unit tests, organisations using CI typically use a build server to implement *continuous* processes of applying [quality control](https://en.wikipedia.org/wiki/Quality_control) in general — small pieces of effort, applied frequently. In addition to running the unit and integration tests, such processes run additional static analyses, measure and profile performance, extract and format documentation from the source code and facilitate manual [QA](https://en.wikipedia.org/wiki/Quality_assurance) processes. On the popular Travis CI service for open-source, only 58.64% of CI jobs execute tests.[[7\]](https://en.wikipedia.org/wiki/Continuous_integration#cite_note-7)

This continuous application of quality control aims to improve the [quality of software](https://en.wikipedia.org/wiki/Software_quality), and to reduce the time taken to deliver it, by replacing the traditional practice of applying quality control *after* completing all development. This is very similar to the original idea of integrating more frequently to make integration easier, only applied to QA processes.

#### CI/CD

Now, CI is often intertwined with [continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery) in a so called CI/CD pipeline. CI makes sure the software checked in on the mainline is always in a state that can be deployed to users and CD makes the deployment process fully automated.



[Travis CI](https://travis-ci.com/plans?gclid=CjwKCAiAzJLzBRAZEiwAmZb0aqBdottiuvAzYRzT-Asxu9ZvIHEJL5nbxnCF757e8mUizSzDVDLUFRoCvOwQAvD_BwE)



[C++환경에서의 CI(지속적통합) 구축 사례.pdf]([file:///home/aimldl/Downloads/%EC%82%AC%EB%A1%80_02_C%20%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C%EC%9D%98%20CI(%EC%A7%80%EC%86%8D%EC%A0%81%ED%86%B5%ED%95%A9)%20%EA%B5%AC%EC%B6%95%20%EC%82%AC%EB%A1%80.pdf](file:///home/aimldl/Downloads/사례_02_C 환경에서의 CI(지속적통합) 구축 사례.pdf), 36 pages, 

통합 개발 환경 구성도 (상세), page 11

<img src="images/CI_implementation_example-CI_environment.png">

통합 개발 환경 흐름도

<img src="images/CI_implementation_example-flow_chart.png">



