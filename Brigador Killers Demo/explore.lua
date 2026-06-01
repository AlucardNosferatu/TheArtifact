-- 数据结构爬取脚本
-- 安全地递归探索对象，防止死循环

local visited = {}
local depth_limit = 3

-- 适配游戏的 print（只接受一个参数）
local function p(str)
    print(str)
end

local function explore(obj, name, depth)
    if depth > depth_limit then
        p(string.rep('  ', depth) .. name .. ' [DEPTH LIMIT]')
        return
    end
    
    local t = type(obj)
    
    -- 打印当前节点
    local indent = string.rep('  ', depth)
    p(indent .. name)
    p(indent .. '  TYPE: ' .. t)
    
    if t == 'table' then
        -- 检查循环引用
        if visited[obj] then
            p(indent .. '  [ALREADY VISITED]')
            return
        end
        visited[obj] = true
        
        -- 遍历表
        local keys = {}
        for k in pairs(obj) do
            table.insert(keys, k)
        end
        table.sort(keys, function(a, b)
            local ta = type(a)
            local tb = type(b)
            if ta ~= tb then
                return ta < tb
            end
            return a < b
        end)
        
        for _, k in ipairs(keys) do
            local v = obj[k]
            local key_str
            if type(k) == 'string' then
                key_str = k
            else
                key_str = '[' .. tostring(k) .. ']'
            end
            explore(v, key_str, depth + 1)
        end
    else
        -- 打印值（如果不是太长）
        local val_str = tostring(obj)
        if #val_str > 100 then
            val_str = val_str:sub(1, 97) .. '...'
        end
        p(indent .. '  VALUE: ' .. val_str)
    end
end

-- 从全局环境开始
p('=== STARTING DATA STRUCTURE EXPLORATION ===')
p('=== GLOBAL ENVIRONMENT (_G) ===')
explore(_G, '_G', 0)
p('=== EXPLORATION COMPLETE ===')
