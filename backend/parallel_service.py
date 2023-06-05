from L05Parallelization.ParallelLauncher import *
from L06Flask.util import *
import pickle,shutil,time,os,io


flask_storage_folder = "flask_storage_folder"

if __name__ == "__main__":
    if not os.path.isdir(flask_storage_folder+"/internal"): os.makedirs(flask_storage_folder+"/internal")
    print("Parallel Service Running")
    while True:
        time.sleep(1)
        new_session_list = [session[0]+"/content.pickle" for session in os.walk(flask_storage_folder+"/internal")]
        for session_file in new_session_list:
            if not os.path.isfile(session_file):continue
            with io.open(session_file,"rb") as session_content: new_session_object = pickle.load(session_content).data
            os.unlink(session_file)
            pipe = new_session_object[SessionKey.pipeline_object] if SessionKey.pipeline_object in new_session_object else None
            data = new_session_object[SessionKey.data_set_object] if SessionKey.data_set_object in new_session_object else None
            result = ResultObject(new_session_object[SessionKey.result_folder]) if SessionKey.result_folder in new_session_object else None
            timeout = 60
            kernel = AvailableAlgorithms.NelderMead
            abort_check = lambda :os.path.isdir(flask_storage_folder+"/abort/"+str(new_session_object[SessionKey.identifier]))
            if SessionKey.optimizer_timeout in new_session_object: timeout = new_session_object[SessionKey.optimizer_timeout]
            if SessionKey.optimizer_kernel in new_session_object: kernel = new_session_object[SessionKey.optimizer_kernel]
            if not pipe and data and result and timeout and kernel: continue
            if not isinstance(timeout,datetime.timedelta): timeout = datetime.timedelta(seconds=timeout)
            try:
                launcher = ParallelLauncher(pipe,data,result,timeout,kernel,abort_check)
                print("Job Detected, Optimizer Running")
                launcher.start()
                print("Job Done")
            except:
                print("Job Aborted")


