from DLLs.Tessng import PyCustomerNet, tessngIFace


# 用户插件子类，代表用户自定义与路网相关的实现逻辑，继承自MyCustomerNet
class MyNet(PyCustomerNet):
    def __init__(self):
        super(MyNet, self).__init__()

    def afterLoadNet(self):
        iface = tessngIFace()
        netiface = iface.netInterface()
        
        # netiface.buildNetGrid(50)

        # info = netiface.netAttrs().otherAttrs()
        # print(info)

    def ref_curvatureMinDist(self, itemType: int, itemId: int, ref_minDist):
        ref_minDist.value = 0.1
        return True


