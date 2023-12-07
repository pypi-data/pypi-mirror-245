# -*- coding: utf-8 -*-
# This file is part of the cashbook-module from m-ds.de for Tryton.
# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
CACHEKEY_ASSETRATE = 'assetrate-%s'


class AssetRate(metaclass=PoolMeta):
    __name__ = 'investment.rate'

    @classmethod
    def create(cls, vlist):
        """ update cache-value
        """
        MemCache = Pool().get('cashbook.memcache')

        records = super(AssetRate, cls).create(vlist)
        for rate in records:
            MemCache.record_update(CACHEKEY_ASSETRATE % rate.asset.id, rate)
        return records

    @classmethod
    def write(cls, *args):
        """ update cache-value
        """
        MemCache = Pool().get('cashbook.memcache')

        super(AssetRate, cls).write(*args)

        actions = iter(args)
        for rates, values in zip(actions, actions):
            for rate in rates:
                MemCache.record_update(CACHEKEY_ASSETRATE % rate.asset.id, rate)

    @classmethod
    def delete(cls, records):
        """ set cache to None
        """
        MemCache = Pool().get('cashbook.memcache')

        for record in records:
            MemCache.record_update(CACHEKEY_ASSETRATE % record.asset.id, None)
        super(AssetRate, cls).delete(records)

# end
