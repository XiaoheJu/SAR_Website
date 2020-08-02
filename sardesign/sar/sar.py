from .rserve import Rpy2
from .data_view import DataViewParser, SarDataView
from .design import SarDesign, DesignParser
from .controller import CentralController
from .input import DjangoInput, CCDInputDesignDeal, CCDInputDataViewDeal, CCDInputAnalyzeDeal
from .output import DjangoOutput, CCDOutDataViewDeal, CCDOutDesignDeal, CCDOutAnalyzeDeal
from .analyze import SarAnalyze, AnalyzeParser
# Django Input Output
in_put = DjangoInput()
out_put = DjangoOutput()

# Rserve
rserve = Rpy2()

# Design
design_parser = DesignParser()
design = SarDesign.instance(parser=design_parser, rserve=rserve)

# Data View
data_view_parser = DataViewParser()
data_view = SarDataView.instance(parser=data_view_parser, rserve=rserve)

# Analyze
analyze_parser = AnalyzeParser()
analyze = SarAnalyze.instance(parser=analyze_parser, rserve=rserve)

# CentralController
controller = CentralController.instance(base_design=design, base_data_view=data_view,
                                        base_analyze=analyze)
controller.set_input_output(base_input=in_put, base_output=out_put)
# CCDDesign
ccd_design_in_deal = CCDInputDesignDeal()
ccd_design_out_deal = CCDOutDesignDeal()

# CCDDataView

ccd_data_view_in_deal = CCDInputDataViewDeal()
ccd_data_view_out_deal = CCDOutDataViewDeal()

# CCDAnalyze

ccd_analyze_in_deal = CCDInputAnalyzeDeal()
ccd_analyze_out_deal = CCDOutAnalyzeDeal()





















# async def produce(queue, n):
#     x = 1
#     while True:
#         x +=1
#         # produce an item
#         print('producing {}/{}'.format(x, n))
#         # simulate i/o operation using sleep
#         await asyncio.sleep(1)
#         item = str(x)
#         # put the item in the queue
#         await queue.put(item)
#
#
#
# async def consume(queue):
#     while True:
#         # wait for an item from the producer
#         item = await queue.get()
#
#         # process the item
#         print('consuming {}...'.format(item))
#         # simulate i/o operation using sleep
#         await asyncio.sleep(3)
#
#         # Notify the queue that the item has been processed
#
#
# async def run(n):
#     queue = asyncio.Queue()
#     # schedule the consumer
#     consumer = asyncio.ensure_future(consume(queue))
#     # run the producer and wait for completion
#     await produce(queue, n)
#     # wait until the consumer has processed all items
#     await queue.join()
#     # the consumer is still awaiting for an item, cancel it
#     consumer.cancel()
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run(10))
# loop.close()

# async def loop_run(loop):
#     pass
#
#
# async def sar():
#
#     await asyncio.sleep(1)
#
#     # sar_queue = TestQueue()
#     # # sar_controller = CentralController.instance(...)
#
#
# if __name__ == "__main__":
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(sar())