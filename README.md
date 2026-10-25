    # SigmaOS-panel

    Taskbar / panel applet host

    Part of the **SigmaOS** sovereign operating-system ecosystem — a multi-repository
    distribution modelled on Linux Mint and Omarchy Linux. See the parent
    [`SigmaOS`](https://github.com/AaryanSinghChauhan09/SigmaOS) repository for the
    full component index.

    ## Upstream inspirations
    - https://github.com/linuxmint/xfce-panel

    ## Design principles applied
    - **Information Hiding**
- **Encapsulation**
- **Fail-Fast**
- **KISS**
- **DRY**
- **Deterministic Testing**

    ## Usage
    Verbs: `applets, add, remove, layout-plan`

    ```
    $ sigma-panel applets
$ sigma-panel add clock --pack end
$ sigma-panel remove clock
$ sigma-panel layout-plan
[start] menu-button > window-list   ~~~panel stretch~~~   [end] sound < clock

    ```

    ## Build & test
    ```
    make build
    make test
    ```

    ## Licence
    GNU General Public License v3.0 (FOSS).
