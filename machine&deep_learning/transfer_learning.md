* Draft: 2020-09-03 (Thu)

[Transfer Learning in SUALAB: 데이터셋 제작부터 Adaptive Transfer Learning까지](https://research.sualab.com/introduction/review/2019/12/19/transfer-learning-in-sualab.html), Dec 19, 2019 • [Introduction](https://research.sualab.com/Introduction.html), [Review](https://research.sualab.com/Review.html) • [기홍도](https://hongdoki.github.io/)

Transfer Learning에 있어서

<img src="http://research.sualab.com/assets/images/transfer-learning-in-sualab/transfer-learning-overview.svg">

ImageNet_pre-trained: Source Data로 ImageNet dataset만 쓴 경우와 

<img src="http://research.sualab.com/assets/images/transfer-learning-in-sualab/transfer-learning-using-imagenet.svg">

SRISC_pre-trained: SuaLab에서 편집한 SRISC (Sualab Research Image Single Classification) Dataset을 쓴 경우 

ImageNet_SRISC_pre-trained: ImageNet과 SRISC를 순차적으로 훈련한 경우

ImageNet-SRISC_joint-pre-trained: ImageNet과 SRISC를 통합하여 훈련한 경우

 타겟 데이터셋의 산업군은 전자부품(electronic component), 음료(beverage), 필름(film), 디스플레이(display)로 다양하게 구성하였습니다. 여러 번 반복 실험한 뒤 **테스트 셋에 대한 오류율(error rate)의 평균**

<img src="http://research.sualab.com/assets/images/transfer-learning-in-sualab/target-err_by_pt-method.svg">

한단계 더 내려가서 

SRISC에서 많은 비중을 차지하고 있던 **PCB** 산업군의 데이터셋만 선별한 **SRISCPCB**를 썼을 경우

<img src="http://research.sualab.com/assets/images/transfer-learning-in-sualab/tl-for-pcb.svg">

전반적으로 성능이 향상되는 것을 보이나, 한 Depth 더 Dataset을 세분화 한 경우엔 성능향상은 없었다고 합니다.

