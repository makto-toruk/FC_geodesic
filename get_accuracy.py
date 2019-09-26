import sys
import time
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='get accuracy for distance matrix')
    parser.add_argument('-d', '--home_dir', type=str,
                        default='/mnt/c/umd/00-fc_unique',
                        help='local or bswift?')
    parser.add_argument('-c1', '--condition1', type=str,
                        help='RS EMOTION GAMBLING LANGUAGE MOTOR RELATIONAL SOCIAL WM; for demo: condition1')
    parser.add_argument('-c2', '--condition2', type=str,
                        help='RS EMOTION GAMBLING LANGUAGE MOTOR RELATIONAL SOCIAL WM; for demo: condition1')
    parser.add_argument('-t', '--trim_method', type=str,
                        default='demo',
                        help='truncated (min) or trim or full; for demo: demo')
    parser.add_argument('-r', '--roi', type=int, 
                        default=300,
                        help='number of ROIs, default: 300')
    parser.add_argument('-m', '--max_workers', type=int, 
                        default=20,
                        help='number of concurrent threads, default: 20')
    parser.add_argument('-b', '--bootstrap', type=int,
                        default=0,
                        help='0: no bootstrap, 1: bootstrap')
    args = parser.parse_args()

    bootstrap = False
    if args.bootstrap == 1:
        bootstrap = True
        
    # load analyzer class
    UTILS_DIR = args.home_dir + '/utils/FC_analyzer'
    sys.path.insert(0, UTILS_DIR)
    from whole_brain_FC_analyzer import accuracy_requestor

    ar = accuracy_requestor(args.condition1, args.condition2,
                            DIR=args.home_dir,
                            max_workers=args.max_workers,
                            trim_method=args.trim_method,
                            kROI=args.roi)
    
    if bootstrap:
        then = time.time()
        # fix inner and outer bootstrap
        ar.make_bootstrap_accuracy_requests(B_outer=1000, b_inner=1000)
        print("elapsed time = %s seconds" %(time.time() - then))
    else:
        then = time.time()
        ar.make_accuracy_requests()
        print("elapsed time = %s seconds" %(time.time() - then))