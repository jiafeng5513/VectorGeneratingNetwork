import time
from progressbar import *

total = 10000


def dosomework():
    time.sleep(0.01)

if __name__ == '__main__':

    # widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(),
    #            ' ', ETA(), ' ', FileTransferSpeed()]
    # pbar = ProgressBar(widgets=widgets, maxval=10 * total).start()
    #
    #
    # for i in range(total):
    #     # do something
    #     pbar.update(10 * i + 1)
    #     dosomework()
    #
    # pbar.finish()
    url="G:/TCIA_LIDC-IDRI/LIDC-IDRI-Sample/LIDC-IDRI-0002/1.3.6.1.4.1.14519.5.2.1.6279.6001.490157381160200744295382098329/1.3.6.1.4.1.14519.5.2.1.6279.6001.619372068417051974713149104919/000001.dcm"
    uuu="G:/TCIA_LIDC-IDRI/LIDC-IDRI-Sample/LIDC-IDRI-0002/1.3.6.1.4.1.14519.5.2.1.6279.6001.490157381160200744295382098329/1.3.6.1.4.1.14519.5.2.1.6279.6001.619372068417051974713149104919"
    print(os.path.dirname(url))
