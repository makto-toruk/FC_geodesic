import sys
import time
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='get distance matrix')
    parser.add_argument('-d', '--home_dir', type=str,
                        default='/mnt/c/umd/demos/FC_geodesic',
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
    args = parser.parse_args()

    # load analyzer class
    UTILS_DIR = args.home_dir + '/utils/FC_analyzer'
    sys.path.insert(0, UTILS_DIR)
    from whole_brain_FC_analyzer import distance_matrix_requestor

    dr = distance_matrix_requestor(args.condition1, args.condition2,
                                   DIR=args.home_dir,
                                   trim_method=args.trim_method,
                                   max_workers=args.max_workers,
                                   kROI=args.roi)
    then = time.time()
    dr.make_distance_requests()
    print("elapsed time = %s seconds" %(time.time() - then))