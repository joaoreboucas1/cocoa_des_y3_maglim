## Running Cosmolike projects <a name="running_cosmolike_projects"></a> 

In this tutorial, we assume the user installed Cocoa via the *Conda installation* method, and the name of the Conda environment is `cocoa`. We also presume the user's terminal is in the folder where Cocoa was cloned.

:one: **Step 1 of 6**: activate the Conda Cocoa environment
    
        $ conda activate cocoa

:two: **Step 2 of 6**: go to the project folder (`./cocoa/Cocoa/projects`) and clone the Cosmolike LSST-Y1 project:
    
        $(cocoa) cd ./cocoa/Cocoa/projects
        $(cocoa) git clone --depth 1 https://github.com/CosmoLike/cocoa_des_y3.git des_y3

:warning: **Warning** :warning: Cocoa developers should drop the shallow clone option `--depth 1`; they should also authenticate to GitHub via SSH keys:

        $(cocoapy38) git clone git@github.com:CosmoLike/cocoa_des_y3.git des_y3
        
By convention, the Cosmolike Organization hosts a Cobaya-Cosmolike project named XXX at `CosmoLike/cocoa_XXX`. However, our scripts and YAML files assume the removal of the `cocoa_` prefix when cloning the repository.
 
:three: **Step 3 of 6**: go back to the Cocoa main folder, and activate the private python environment
    
        $(cocoapy38) cd ../
        $(cocoapy38) source start_cocoa
 
:warning: (**warning**) :warning: Remember to run the start_cocoa script only after cloning the project repository. The script *start_cocoa* creates the necessary symbolic links and adds the *Cobaya-Cosmolike interface* of all projects to `LD_LIBRARY_PATH` and `PYTHONPATH` paths.

:four: **Step 4 of 6**: compile the project
 
        $(cocoapy38)(.local) source ./projects/des_y3/scripts/compile_des_y3

:five: **Step 5 of 6**: select the number of OpenMP cores
    
        $(cocoapy38)(.local) export OMP_PROC_BIND=close; export OMP_NUM_THREADS=4
        
:five:  **Step 6 of 6**: run a template YAML file

One model evaluation:

        $(cocoapy38)(.local) mpirun -n 1 --oversubscribe --mca btl vader,tcp,self --bind-to core:overload-allowed --rank-by core --map-by numa:pe=${OMP_NUM_THREADS} cobaya-run ./projects/des_y3/EXAMPLE_EVALUATE1.yaml -f
 
MCMC:

        $(cocoapy38)(.local) mpirun -n 4 --oversubscribe --mca btl vader,tcp,self --bind-to core:overload-allowed --rank-by core --map-by numa:pe=${OMP_NUM_THREADS} cobaya-run ./projects/des_y3/EXAMPLE_MCMC1.yaml -f

## Deleting Cosmolike projects <a name="running_cosmolike_projects"></a>

:warning: (**warning**) :warning: Never delete the `des_y3` folder from the project folder without running `stop_cocoa` first; otherwise, Cocoa will have ill-defined soft links at `Cocoa/cobaya/cobaya/likelihoods/` , `Cocoa/external_modules/code/` and `Cocoa/external_modules/data/`
