def entry_point():
    pass
    # select an event in current event_pool
    # execute that event
    # update flags by pool_flags
    # read chain_status
    # if chain_status is not None
    #     read pool_status
    #     check pools jumper with flags
    #     if pools_jumper is triggered
    #         if this pool is an end of this chain, this chain should end
    #             chain_status to None
    #             pool_status to None
    #         else:
    #             pool_status to next_pool_status, chain is unchanged, but pool is changed (follow plot map)
    #     else:
    #         keep pool unchanged
    # else:
    #     check all chain_trigger
    #     gather all triggered chain
    #     if there is at least one triggered chain
    #         select chain with the highest priority
    #         chain_status changed to the selected chain
    #         pool_status changed to the beginning pool of the selected chain
    #     else:
    #         nothing changed, no chain, default pool
